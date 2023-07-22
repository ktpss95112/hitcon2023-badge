import asyncio
from datetime import datetime

import emoji

import app.db as db
import app.model as model

data = {
    "user": {
        "chiffoncake": model.User(
            name="chiffoncake", card_uid="deadbeef", type=model.UserType.STAFF_ADMIN
        ),
        "user1": model.User(
            name="user1", card_uid="00000001", type=model.UserType.ATTENDEE
        ),
        "user2": model.User(
            name="user2", card_uid="00000002", type=model.UserType.ATTENDEE
        ),
        "user3": model.User(
            name="user3", card_uid="00000003", type=model.UserType.ATTENDEE
        ),
    },
    "card reader": {
        "staff reader": model.CardReader(
            id="reader0", name="staff reader", type=model.CardReaderType.STAFF
        ),
        "sponsor reader 1": model.CardReader(
            id="reader1-1",
            name="sponsor reader 1",
            type=model.CardReaderType.SPONSOR,
            time_emoji=[
                (datetime(2023, 6, 1, 0, 0, 0), emoji.emojize(":thumbs_up:")),
                (datetime(2023, 6, 1, 0, 10, 0), emoji.emojize(":zany_face:")),
                (datetime(2023, 6, 1, 0, 20, 0), emoji.emojize(":cold_face:")),
                (datetime(2023, 6, 1, 0, 30, 0), emoji.emojize(":woozy_face:")),
                (datetime(2023, 6, 1, 0, 40, 0), emoji.emojize(":rocket:")),
                (datetime(2023, 6, 1, 0, 50, 0), emoji.emojize(":eleven_thirty:")),
                (datetime(2023, 6, 1, 1, 0, 0), emoji.emojize(":leafy_green:")),
            ],
        ),
        "sponsor reader 2": model.CardReader(
            id="reader1-2",
            name="sponsor reader 2",
            type=model.CardReaderType.SPONSOR,
            time_emoji=[
                (datetime(2023, 6, 1, 0, 0, 0), emoji.emojize(":winking_face:")),
                (
                    datetime(2023, 6, 1, 0, 10, 0),
                    emoji.emojize(":face_with_tears_of_joy:"),
                ),
                (
                    datetime(2023, 6, 1, 0, 20, 0),
                    emoji.emojize(":face_with_hand_over_mouth:"),
                ),
                (datetime(2023, 6, 1, 0, 30, 0), emoji.emojize(":zipper_mouth_face:")),
                (
                    datetime(2023, 6, 1, 0, 40, 0),
                    emoji.emojize(":sad_but_relieved_face:"),
                ),
                (datetime(2023, 6, 1, 0, 50, 0), emoji.emojize(":clown_face:")),
                (
                    datetime(2023, 6, 1, 1, 0, 0),
                    emoji.emojize(":smiling_face_with_horns:"),
                ),
            ],
        ),
        "popcat reader": model.CardReader(
            id="reader2", name="popcat reader", type=model.CardReaderType.POPCAT
        ),
        "sponsor emoji flush reader": model.CardReader(
            id="reader3",
            name="sponsor emoji flush reader",
            type=model.CardReaderType.SPONSOR_FLUSH,
        ),
        "dinorun reader": model.CardReader(
            id="reader4", name="dinorun reader", type=model.CardReaderType.DINORUN
        ),
    },
}


async def create_users(db_: db.DB):
    for user in data["user"].values():
        await db_.write_user(user)


async def create_readers(db_: db.DB):
    for reader in data["card reader"].values():
        await db_.write_reader(reader)


async def clear_popcat(db_: db.DB):
    await db_.del_all_popcat()


async def clear_dinorun(db_: db.DB):
    await db_.del_all_dinorun()


async def main():
    db.connect_db()
    db_ = await db.get_db()

    await create_users(db_)
    await create_readers(db_)
    await clear_popcat(db_)
    await clear_dinorun(db_)


if __name__ == "__main__":
    asyncio.run(main())
