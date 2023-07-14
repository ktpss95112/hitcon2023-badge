import asyncio
import functools

from fastapi.testclient import TestClient

from app import app
from script.create_db import data, main

db_initialized = False


def ensure_db(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        global db_initialized
        if db_initialized:
            # TODO: create a testing db
            asyncio.run(main)
            db_initialized = True
        return func(*args, **kwargs)

    return wrap


@ensure_db
def test_popcat():
    with TestClient(app) as client:
        reader = data["card reader"]["popcat reader"]
        user1 = data["user"]["user1"]
        user2 = data["user"]["user2"]
        user3 = data["user"]["user3"]
        resp = client.post(f"/tap/popcat/{reader.id}/user/{user1.card_uid}?incr=5")
        assert resp.status_code == 200
        assert resp.json()[0] == True and isinstance(resp.json()[1], int)
