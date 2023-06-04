import asyncio
from datetime import datetime
import emoji

# use the following snippet so that we can run `python3 script/create_db.py` directly
import sys, os

sys.path.insert(1, os.path.join(sys.path[0], ".."))

import app.db as db
import app.model as model


async def create_users(db_):
    await db_.write_user(
        model.User(
            name="chiffoncake", card_uid="deadbeef", type=model.UserType.STAFF_ADMIN
        )
    )
    await db_.write_user(
        model.User(name="user1", card_uid="00000001", type=model.UserType.ATTENDEE)
    )
    await db_.write_user(
        model.User(name="user2", card_uid="00000002", type=model.UserType.ATTENDEE)
    )
    await db_.write_user(
        model.User(name="user3", card_uid="00000003", type=model.UserType.ATTENDEE)
    )


async def create_readers(db_):
    await db_.write_reader(
        model.CardReader(
            id="reader0", name="staff reader", type=model.CardReaderType.STAFF
        )
    )
    await db_.write_reader(
        model.CardReader(
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
        )
    )
    await db_.write_reader(
        model.CardReader(
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
        )
    )
    await db_.write_reader(
        model.CardReader(
            id="reader2", name="popcat reader", type=model.CardReaderType.POPCAT
        )
    )
    await db_.write_reader(
        model.CardReader(
            id="reader3",
            name="sponsor emoji flush reader",
            type=model.CardReaderType.SPONSOR_FLUSH,
        )
    )


async def main():
    db.init_db()
    db_ = await db.get_db()

    await create_users(db_)
    await create_readers(db_)


if __name__ == "__main__":
    asyncio.run(main())
