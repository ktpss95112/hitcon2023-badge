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
        if not db_initialized:
            # TODO: create a testing db
            asyncio.run(main())
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

        scores = [7, -1, 5]
        users = [user1, user2, user3]
        for score, user in zip(scores, users):
            # test push score
            resp = client.post(
                f"/tap/popcat/{reader.id}/user/{user.card_uid}?incr={score}"
            )
            assert resp.status_code == 200
            rj = resp.json()
            assert rj[0] == True and isinstance(rj[1], int)

            # test get score
            resp = client.get(f"/popcat/{user.card_uid}")
            assert resp.status_code == 200
            rj = resp.json()
            assert rj == score

        # test if the cooldown works
        resp = client.post(f"/tap/popcat/{reader.id}/user/{user.card_uid}?incr={score}")
        assert resp.status_code == 200
        rj = resp.json()
        assert rj[0] == False and isinstance(rj[1], int)

        # test all
        resp = client.get(f"/popcat/")
        assert resp.status_code == 200
        rj = resp.json()
        for score, user in zip(scores, users):
            assert rj[user.card_uid] == score
            del rj[user.card_uid]
        assert len(rj) == 0


@ensure_db
def test_dinorun():
    with TestClient(app) as client:
        reader = data["card reader"]["dinorun reader"]
        user1 = data["user"]["user1"]
        user2 = data["user"]["user2"]
        user3 = data["user"]["user3"]
        all_users = [user1, user2, user3]

        scores = [7.5, 100.235, 5, 300.0, 0.1]
        users = [user1, user2, user3, user1, user2]
        expecteds = [7.5, 100.235, 5, 300.0, 100.235]
        for score, user, expected in zip(scores, users, expecteds):
            # test push score
            print(f"/dinorun/{user.card_uid}?score={score}")
            resp = client.post(f"/dinorun/{user.card_uid}?score={score}")
            assert resp.status_code == 200
            rj = resp.json()
            assert rj == True

            # test get score
            resp = client.get(f"/dinorun/{user.card_uid}")
            assert resp.status_code == 200
            rj = resp.json()
            assert rj == expected

        # test all
        resp = client.get(f"/dinorun/")
        assert resp.status_code == 200
        rj = resp.json()
        for user in all_users:
            highest_score = max(
                score for score, user_ in zip(scores, users) if user_ == user
            )
            assert rj[user.card_uid] == highest_score
            del rj[user.card_uid]
        assert len(rj) == 0