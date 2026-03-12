import os
import sqlite3
import json
import time
import urllib.request
import urllib.parse
from importlib.resources import files
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

static_path = files("darkglass").joinpath("static")
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

DB_PATH = "darkglass.db"
# admin email whitelist; empty list means any authenticated Google user
# (a `[roles]` section in the config may replace this list entirely)
ADMIN_EMAILS: list[str] = []
# configuration populated from darkglass.toml
GOOGLE_CLIENT_ID: Optional[str] = None
GOOGLE_CLIENT_SECRET: Optional[str] = None


def load_config() -> dict:
    path = "darkglass.toml"
    if not os.path.exists(path):
        return {}
    try:
        import tomllib
    except ImportError:
        return {}
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except Exception:
        return {}


_CONFIG = load_config()

gemini_section = _CONFIG.get("gemini", {}) or {}
GEMINI_API_KEY = gemini_section.get("api_key")
GEMINI_MODEL = gemini_section.get("model") or "gemini-3.1-flash-lite-preview"

context_section = _CONFIG.get("context", {}) or {}
SYSTEM_PROMPT = (
    context_section.get("prompt")
    or "Answer prospective student questions using the knowledge you have."
)

# google configuration may be provided in a [google] section of the
# config file; values are optional and fall back to the hardcoded defaults
# above.  only the client ID is required for the token‑based flow.
google_section = _CONFIG.get("google", {}) or {}
GOOGLE_CLIENT_ID = google_section.get("client_id")
GOOGLE_CLIENT_SECRET = google_section.get("client_secret")

# roles section may contain an `admins` list which overrides the default
# behaviour described above.  if present it replaces `ADMIN_EMAILS`.
roles_section = _CONFIG.get("roles", {}) or {}
ADMIN_EMAILS = roles_section.get("admins", []) or ADMIN_EMAILS


def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts INTEGER,
            user_message TEXT,
            assistant_message TEXT
        )
        """
    )
    conn.commit()
    return conn


init_db()


def verify_google_token(id_token: str) -> Optional[str]:
    """Verify an OAuth2 ID token with Google and return the user's email.

    Google provides a simple endpoint for validating ID tokens:
    https://oauth2.googleapis.com/tokeninfo?id_token=<token>

    The response includes the `email` and an `aud` field which should match
    our configured client ID when available.  We make a blocking HTTP call
    rather than introducing any additional dependencies.

    Returns the email address if verification succeeds, otherwise ``None``.
    """
    try:
        url = "https://oauth2.googleapis.com/tokeninfo?id_token=" + urllib.parse.quote(
            id_token
        )
        resp = urllib.request.urlopen(url)
        info = json.load(resp)
        # if a client ID is configured, enforce audience match
        aud = info.get("aud")
        if GOOGLE_CLIENT_ID and aud != GOOGLE_CLIENT_ID:
            return None
        return info.get("email")
    except Exception:
        return None


def current_user(authorization: Optional[str] = Header(None)) -> Optional[str]:
    """Extract the current user email from an Authorization header.

    The frontend is expected to obtain a Google ID token and present it as a
    bearer token.  We verify it on every request via
    :func:`verify_google_token`.
    """
    if not authorization:
        return None
    if authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
        return verify_google_token(token)
    return None


def require_admin(user: Optional[str] = Depends(current_user)):
    if not user or (ADMIN_EMAILS and user not in ADMIN_EMAILS):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


@app.post("/chat")
def chat_endpoint(payload: dict):
    message = payload.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="message is required")
    answer = call_model(message)
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO interactions (ts, user_message, assistant_message) VALUES (?, ?, ?)",
        (int(time.time()), message, answer),
    )
    conn.commit()
    return {"answer": answer}


@app.get("/logs")
def get_logs(user: str = Depends(require_admin)):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM interactions ORDER BY ts DESC")
    rows = c.fetchall()
    return [dict(row) for row in rows]


@app.get("/admin", response_class=HTMLResponse)
def admin_page():
    """Serve the admin dashboard HTML.

    The page itself is public; authentication happens in JavaScript using a
    Google-issued ID token.  A placeholder in the static file is replaced
    with the configured client ID so the script can initialize the Google
    sign‑in widget.
    """
    if not GOOGLE_CLIENT_ID:
        return HTMLResponse("<h1>Google OAuth not configured</h1>")
    try:
        with open("static/admin.html") as f:
            html = f.read()
        return HTMLResponse(html.replace("__GOOGLE_CLIENT_ID__", GOOGLE_CLIENT_ID))
    except FileNotFoundError:
        return HTMLResponse("<h1>admin page not found</h1>")


def call_model(message: str) -> str:
    key = GEMINI_API_KEY
    if not key:
        return "[no API key configured]"
    model = GEMINI_MODEL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    headers = {"Content-Type": "application/json", "x-goog-api-key": key}
    prompt_text = f"{SYSTEM_PROMPT}\n\n{message}" if SYSTEM_PROMPT else message
    data = {"contents": [{"parts": [{"text": prompt_text}]}]}
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        j = json.load(resp)
        return j["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"[error calling model: {e}]"
    return ""
