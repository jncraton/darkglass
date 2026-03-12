import os
import tempfile
import sqlite3
import importlib
import json
from pathlib import Path
from fastapi.testclient import TestClient


def load_app_with_config(toml_contents: str | None = None):
    if toml_contents is not None:
        temp = tempfile.TemporaryDirectory()
        old_cwd = os.getcwd()
        os.chdir(temp.name)
        Path("darkglass.toml").write_text(toml_contents)
    try:
        if "darkglass.main" in importlib.sys.modules:
            importlib.reload(importlib.import_module("darkglass.main"))
        mod = importlib.import_module("darkglass.main")
        client = TestClient(mod.app)
        return mod, client
    finally:
        if toml_contents is not None:
            os.chdir(old_cwd)
            temp.cleanup()


def test_chat_no_message():
    mod, client = load_app_with_config()
    r = client.post("/chat", json={})


def test_login_not_configured():
    mod, client = load_app_with_config()
    r = client.get("/login")
    assert r.status_code == 500
    assert r.json()["detail"] == "Google OAuth not configured"


def test_login_with_config():
    toml = """
    [google]
    client_id = "abc"
    client_secret = "def"
    """
    mod, client = load_app_with_config(toml)
    assert mod.GOOGLE_CLIENT_ID == "abc"
    assert mod.GOOGLE_CLIENT_SECRET == "def"
    # default redirect stays the same
    assert mod.OAUTH_REDIRECT == "http://localhost:8000/auth/callback"
    r = client.get("/login")
    assert r.status_code == 307
    location = r.headers["location"]
    assert "client_id=abc" in location
    assert "redirect_uri=" in location


def test_login_redirect_override():
    toml = """
    [google]
    client_id = "abc"
    client_secret = "def"
    redirect = "https://example.com/cb"
    """
    mod, client = load_app_with_config(toml)
    assert mod.OAUTH_REDIRECT == "https://example.com/cb"
    r = client.get("/login")
    assert r.status_code == 307
    location = r.headers["location"]
    assert "redirect_uri=https%3A%2F%2Fexample.com%2Fcb" in location
