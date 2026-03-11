import os
import tempfile
import sqlite3
from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_chat_no_message():
    r = client.post('/chat', json={})
    assert r.status_code == 400


def test_chat_logging(tmp_path, monkeypatch):
    # set up temporary db
    dbfile = tmp_path / 'data.db'
    monkeypatch.setenv('DB_PATH', str(dbfile))
    # ensure init is called
    main.init_db()
    # also monkeypatch model call to return static value
    monkeypatch.setattr(main, 'call_model', lambda msg: 'reply')
    r = client.post('/chat', json={'message': 'hello'})
    assert r.status_code == 200
    assert r.json()['answer'] == 'reply'
    # check database entry
    conn = sqlite3.connect(str(dbfile))
    c = conn.cursor()
    c.execute('SELECT user_message,assistant_message FROM interactions')
    rows = c.fetchall()
    assert rows == [('hello', 'reply')]
