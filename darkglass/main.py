import os
import sqlite3
import json
import time
import hmac
import hashlib
import urllib.request
import urllib.parse
from typing import Optional

from fastapi import FastAPI, Request, Response, HTTPException, Depends, Cookie
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

DB_PATH = "data.db"
sessions = {}
ADMIN_EMAILS: list[str] = []
COOKIE_NAME = "admin_session"
COOKIE_SECRET = "secret"
GOOGLE_CLIENT_ID: Optional[str] = None
GOOGLE_CLIENT_SECRET: Optional[str] = None

# google oauth redirect fixed default
OAUTH_REDIRECT = "http://localhost:8000/auth/callback"


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


def sign_value(value: str) -> str:
    sig = hmac.new(COOKIE_SECRET.encode(), value.encode(), hashlib.sha256).hexdigest()
    return f"{value}|{sig}"


def verify_signed(s: str) -> Optional[str]:
    if "|" not in s:
        return None
    value, sig = s.rsplit("|", 1)
    expected = hmac.new(
        COOKIE_SECRET.encode(), value.encode(), hashlib.sha256
    ).hexdigest()
    if hmac.compare_digest(expected, sig):
        return value
    return None


def current_user(session: Optional[str] = Cookie(None)) -> Optional[str]:
    if not session:
        return None
    token = verify_signed(session)
    if not token:
        return None
    return sessions.get(token)


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
def admin_page(user: str = Depends(require_admin)):
    try:
        with open("static/admin.html") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse("<h1>admin page not found</h1>")


@app.get("/login")
def login_redirect():
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google OAuth not configured")
    base = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "response_type": "code",
        "scope": "openid email",
        "redirect_uri": OAUTH_REDIRECT,
        "access_type": "offline",
        "prompt": "consent",
    }
    url = f"{base}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)


@app.get("/auth/callback")
def auth_callback(code: Optional[str] = None, response: Response = None):
    if not code:
        raise HTTPException(status_code=400, detail="code is required")
    data = urllib.parse.urlencode(
        {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": OAUTH_REDIRECT,
            "grant_type": "authorization_code",
        }
    ).encode()
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    resp = urllib.request.urlopen(req)
    token_info = json.load(resp)
    access_token = token_info.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="failed to obtain access token")

    req2 = urllib.request.Request(
        f"https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token={urllib.parse.quote(access_token)}"
    )
    resp2 = urllib.request.urlopen(req2)
    userinfo = json.load(resp2)
    email = userinfo.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="email not provided")
    token = hashlib.sha256(os.urandom(32)).hexdigest()
    sessions[token] = email
    signed = sign_value(token)
    response = RedirectResponse("/admin")
    response.set_cookie(COOKIE_NAME, signed, httponly=True)
    return response


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


@app.get("/")
def index():
    html = """
    <html><head><title>Darkglass</title></head>
    <body>
    <h1>Darkglass</h1>
    <p>Include <code>&lt;script src=\"/static/widget.js\"&gt;&lt;/script&gt;</code> to embed chat widget.</p>
    </body></html>
    """
    return HTMLResponse(html)
