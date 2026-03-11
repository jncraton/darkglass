import os
import tempfile
import sqlite3
from fastapi.testclient import TestClient

from darkglass import main

client = TestClient(main.app)


def test_chat_no_message():
    r = client.post('/chat', json={})
    assert r.status_code == 400
