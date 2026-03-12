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
