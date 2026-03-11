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
    assert r.status_code == 400


def test_config_file_overrides_environment(tmp_path, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("SYSTEM_PROMPT", raising=False)
    cfg = """
    gemini_api_key = "configkey"
    prompt = "config prompt text"
    """
    mod, client = load_app_with_config(cfg)
    assert mod.GEMINI_API_KEY == "configkey"
    assert mod.SYSTEM_PROMPT == "config prompt text"


def test_environment_fallback(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "envkey")
    monkeypatch.setenv("SYSTEM_PROMPT", "env prompt")
    mod, client = load_app_with_config()
    assert mod.GEMINI_API_KEY == "envkey"
    assert mod.SYSTEM_PROMPT == "env prompt"


def test_call_model_builds_prompt(monkeypatch):
    cfg = """
    gemini_api_key = "k"
    prompt = "PREAMBLE"
    """
    mod, client = load_app_with_config(cfg)
    captured = {}

    class DummyResp:
        def __init__(self):
            self._body = json.dumps(
                {"candidates": [{"content": {"parts": [{"text": "reply"}]}}]}
            ).encode()

        def read(self):
            return self._body

    def fake_urlopen(req, timeout=None):
        try:
            data = req.data.decode()
        except Exception:
            data = None
        captured["url"] = req.full_url
        captured["headers"] = req.headers
        captured["data"] = json.loads(data) if data else None
        return DummyResp()

    monkeypatch.setattr("darkglass.main.urllib.request.urlopen", fake_urlopen)
    answer = mod.call_model("question")
    assert answer == "reply"
    text = captured["data"]["contents"][0]["parts"][0]["text"]
    assert text.startswith("PREAMBLE")
    assert captured["headers"]["x-goog-api-key"] == "k"
