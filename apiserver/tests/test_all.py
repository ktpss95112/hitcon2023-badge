import asyncio
import functools
from collections import Counter

from fastapi.testclient import TestClient

from app import app
from app.model import (
    ActivityDate,
    CryptoRedeemRecord,
    DinorunRecord,
    EmojiRecord,
    PopcatRecord,
)
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

        # test if user without any record works properly
        users = [user1, user2, user3]
        for user in users:
            resp = client.get(f"/popcat/{user.card_uid}/score")
            assert resp.status_code == 200
            rj = resp.json()
            assert rj == 0
            resp = client.get(f"/popcat/{user.card_uid}/record")
            assert resp.status_code == 200
            rj = resp.json()
            assert rj == []

        scores = [7, -1, 5]
        users = [user1, user2, user3]
        for score, user in zip(scores, users):
            # test push score
            resp = client.post(
                f"/tap/popcat/{reader.id}/user/{user.card_uid}?incr={score}"
            )
            assert resp.status_code == 200
            rj = resp.json()
            assert rj[0] is True and isinstance(rj[1], int)

            # test get score
            resp = client.get(f"/popcat/{user.card_uid}/score")
            assert resp.status_code == 200
            rj = resp.json()
            assert rj == score
            resp = client.get(f"/popcat/{user.card_uid}/record")
            assert resp.status_code == 200
            record = PopcatRecord.parse_obj(resp.json()[0])
            assert record.card_uid == user.card_uid
            assert record.incr == score

        # test if the cooldown works
        resp = client.post(f"/tap/popcat/{reader.id}/user/{user.card_uid}?incr={score}")
        assert resp.status_code == 200
        rj = resp.json()
        assert rj[0] == False and isinstance(rj[1], int)

        # test all record
        resp = client.get(f"/popcat")
        assert resp.status_code == 200
        rj = resp.json()
        assert len(rj) == len(users)

        # test all score
        resp = client.get(f"/popcat/score")
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

        # test if user without any record works properly
        users = [user1, user2, user3]
        for user in users:
            resp = client.get(f"/dinorun/{user.card_uid}/score")
            assert resp.status_code == 200
            rj = resp.json()
            assert rj == 0
            resp = client.get(f"/dinorun/{user.card_uid}/record")
            assert resp.status_code == 200
            rj = resp.json()
            assert rj == []

        scores = [7.5, 100.235, 5, 300.0, 0.1]
        users = [user1, user2, user3, user1, user2]
        expecteds = [7.5, 100.235, 5, 300.0, 100.235]
        for i, (score, user, expected) in enumerate(zip(scores, users, expecteds)):
            # test push score
            resp = client.post(f"/dinorun/{user.card_uid}?score={score}")
            assert resp.status_code == 200
            rj = resp.json()
            assert rj is True

            # test get score
            resp = client.get(f"/dinorun/{user.card_uid}/score")
            assert resp.status_code == 200
            rj = resp.json()
            assert rj == expected
            resp = client.get(f"/dinorun/{user.card_uid}/record")
            assert resp.status_code == 200
            rj = resp.json()
            assert len(rj) == users[: i + 1].count(user)
            assert all(
                DinorunRecord.parse_obj(record).card_uid == user.card_uid
                for record in rj
            )

        # test all record
        resp = client.get(f"/dinorun/")
        assert resp.status_code == 200
        rj = resp.json()
        assert len(rj) == len(users)

        # test all score
        resp = client.get(f"/dinorun/score")
        assert resp.status_code == 200
        rj = resp.json()
        for user in all_users:
            highest_score = max(
                score for score, user_ in zip(scores, users) if user_ == user
            )
            assert rj[user.card_uid] == highest_score
            del rj[user.card_uid]
        assert len(rj) == 0


@ensure_db
def test_tap():
    with TestClient(app) as client:
        counter = Counter()
        for user in data["user"].values():
            counter[user] = len(
                client.get(f"/tap/tap_record/user/{user.card_uid}").json()
            )
        for reader in data["card reader"].values():
            counter[reader] = len(
                client.get(f"/tap/tap_record/cardreader/{reader.id}").json()
            )

        def test(url_prefix, reader, user, **kwargs):
            card_uid = user.card_uid
            reader_id = reader.id

            curr_len_user = len(client.get(f"/tap/tap_record/user/{card_uid}").json())
            curr_len_reader = len(
                client.get(f"/tap/tap_record/cardreader/{reader_id}").json()
            )
            curr_len_user_reader = len(
                client.get(
                    f"/tap/tap_record/user/{card_uid}/cardreader/{reader_id}"
                ).json()
            )

            assert curr_len_user == counter[user]
            assert curr_len_reader == counter[reader]

            resp = client.post(f"{url_prefix}/{reader_id}/user/{card_uid}", **kwargs)
            assert resp.status_code == 200

            new_len_user = len(client.get(f"/tap/tap_record/user/{card_uid}").json())
            new_len_reader = len(
                client.get(f"/tap/tap_record/cardreader/{reader_id}").json()
            )
            new_len_user_reader = len(
                client.get(
                    f"/tap/tap_record/user/{card_uid}/cardreader/{reader_id}"
                ).json()
            )
            assert new_len_user == curr_len_user + 1
            assert new_len_reader == curr_len_reader + 1
            assert new_len_user_reader == curr_len_user_reader + 1

            counter[user] += 1
            counter[reader] += 1

        test(
            "/tap/sponsor",
            data["card reader"]["sponsor reader 1"],
            data["user"]["chiffoncake"],
        )
        test(
            "/tap/sponsor",
            data["card reader"]["sponsor reader 2"],
            data["user"]["chiffoncake"],
        )
        test(
            "/tap/sponsor",
            data["card reader"]["sponsor reader 1"],
            data["user"]["user1"],
        )
        test(
            "/tap/sponsor",
            data["card reader"]["sponsor reader 2"],
            data["user"]["user1"],
        )
        test(
            "/tap/popcat",
            data["card reader"]["popcat reader"],
            data["user"]["user1"],
            params={"incr": "10"},
        )
        test(
            "/tap/popcat",
            data["card reader"]["popcat reader"],
            data["user"]["user2"],
            params={"incr": "10"},
        )
        test(
            "/tap/sponsor_flush_emoji",
            data["card reader"]["sponsor emoji flush reader"],
            data["user"]["user1"],
            json={"emoji_list": "aaa"},
        )
        test(
            "/tap/sponsor_flush_emoji",
            data["card reader"]["sponsor emoji flush reader"],
            data["user"]["user2"],
            json={"emoji_list": "aaa"},
        )
        test("/tap/crypto", data["card reader"]["crypto reader"], data["user"]["user1"])
        test("/tap/crypto", data["card reader"]["crypto reader"], data["user"]["user2"])


@ensure_db
def test_emoji():
    with TestClient(app) as client:
        reader = data["card reader"]["sponsor emoji flush reader"]
        user1 = data["user"]["user1"]
        user2 = data["user"]["user2"]
        user3 = data["user"]["user3"]
        users = [user1, user2, user3]

        resp = client.get(f"/emoji")
        assert resp.status_code == 200
        len_ = len(resp.json())

        for user in users:
            resp = client.post(
                f"/tap/sponsor_flush_emoji/{reader.id}/user/{user.card_uid}",
                json={"emoji_list": "abc"},
            )
            assert resp.status_code == 200
            assert resp.json()

            resp = client.get(f"/emoji")
            assert resp.status_code == 200
            assert len(resp.json()) == len_ + 1
            assert all(EmojiRecord.parse_obj(record) for record in resp.json())
            len_ += 1


@ensure_db
def test_crypto():
    with TestClient(app) as client:
        reader = data["card reader"]["crypto reader"]
        user1 = data["user"]["user1"]
        user2 = data["user"]["user2"]
        user3 = data["user"]["user3"]
        users = [user1, user2, user3]
        dates = [ActivityDate.fisrt, ActivityDate.second]

        resp = client.get("/crypto")
        assert resp.status_code == 200
        assert isinstance((rj := resp.json()), list) and len(rj) == 0

        for user, date in zip(users, dates):
            resp = client.get(f"/crypto/user/{user.card_uid}/date/{date}")
            assert resp.status_code == 200
            assert resp.json() is None

        for i, (user, date) in enumerate(zip(users, dates)):
            resp = client.post(f"/crypto/user/{user.card_uid}/date/{date}")
            assert resp.status_code == 200
            assert resp.json() is True

            resp = client.get("/crypto")
            assert resp.status_code == 200
            assert isinstance((rj := resp.json()), list) and len(rj) == i + 1

        for user, date in zip(users, dates):
            resp = client.get(f"/crypto/user/{user.card_uid}/date/{date}")
            assert resp.status_code == 200
            record = CryptoRedeemRecord.parse_obj(resp.json())
            assert record.card_uid == user.card_uid
            assert record.date == date

        resp = client.get("/crypto")
        assert resp.status_code == 200
        rj = resp.json()
        all_key = set((user.card_uid, date) for user, date in zip(users, dates))
        for record in map(CryptoRedeemRecord.parse_obj, rj):
            all_key.remove((record.card_uid, record.date))
        assert len(all_key) == 0


@ensure_db
def test_read_emoji_table():
    with TestClient(app) as client:
        reader1 = data["card reader"]["sponsor reader 1"]
        reader2 = data["card reader"]["sponsor reader 2"]

        for reader in [reader1, reader2]:
            all_ = set()
            for day in (1, 2):
                for part in range(4):
                    resp = client.get(
                        f"/cardreader/emoji_time_table/{reader.id}/day/{day}/part/{part}"
                    )
                    assert resp.status_code == 200
                    rj = resp.json()
                    for dt, emoji in rj:
                        all_.add((dt, emoji))

            resp = client.get(f"/cardreader/emoji_time_table/{reader.id}")
            assert resp.status_code == 200
            rj = resp.json()
            print(rj)
            assert all_ == set([(dt, emoji) for dt, emoji in rj])
