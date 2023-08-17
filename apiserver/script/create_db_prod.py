import argparse
import asyncio
import random
from datetime import datetime, timedelta
from pathlib import Path

import app.db as db
from app.model import CardReader, CardReaderType, User, UserType


async def handle_uid_file(db_: db.DB, uid_file: Path):
    with uid_file.open("r") as fp:
        content = fp.read().strip()

    uids = content.split("\n")
    for uid in uids:
        await db_.write_user(User(card_uid=uid, name=uid, type=UserType.ATTENDEE))


def gen_readers():
    # fmt: off
    all_emojis = ['😂', '🤣', '👍', '😭', '🙏', '😘', '🥰', '😍', '😊', '🎉', '😁', '💕', '🥺', '😅', '🔥', '🤦', '🤷', '🙄', '😆', '🤗', '😉', '🎂', '🤔', '👏', '🙂', '😳', '🥳', '😎', '👌', '💜', '😔', '💪', '💖', '👀', '😋', '😏', '😢', '👉', '💗', '😩', '💯', '🌹', '💞', '🎈', '💙', '😃', '💐', '😜', '🙈', '🤞', '😄', '🤤', '🙌', '🤪', '😀', '💋', '💀', '👇', '💔', '😌', '💓', '🤩', '🙃', '😬', '😱', '😴', '🤭', '😐', '🌞', '😒', '😇', '🌸', '😈', '🎶', '🎊', '🥵', '😞', '💚', '🖤', '💰', '😚', '👑', '🎁', '💥', '🙋', '😑', '🥴', '👈', '👋', '🤮', '😤', '🤢', '🌟', '😥', '🌈', '💛', '😝', '😫', '😲', '🔴', '🌻', '🤯', '💃', '👊', '🤬', '🏃', '😕', '🍀', '💦', '🦋', '🤨', '🌺', '😹', '🤘', '🌷', '💝', '💤', '🤝', '🐰', '😓', '💘', '🍻', '😟', '😣', '🧐', '🤠', '😻', '🌙', '😛', '🤙', '🙊', '🧡', '🤡', '🤫', '🌼', '🥂', '😷', '🤓', '🥶', '😶', '😖', '🎵', '🚶', '😙', '🍆', '🤑', '💅', '😗', '🐶', '🍓', '👅', '👄', '🌿', '🚨', '📣', '🤟', '🍑', '🍃', '😮', '💎', '📢', '🌱', '🙁', '🍷', '😪', '🌚', '🏆', '🍒', '💉', '🛒', '😸', '🐾', '👎', '🚀', '🎯', '🍺', '📌', '📷', '🙇', '💨', '🍕', '🏠', '📸', '🐇', '🚩', '😰', '👶', '🌊', '🐕', '💫', '😵', '🎤', '🏡', '🥀', '🤧', '🍾', '🍰', '🍁', '🤲', '👆', '😯', '💌', '💸', '🧁', '🕺', '😺', '💧', '💣', '🤐', '🍎', '🐷', '🐥', '💁', '📍', '🎀', '🙅', '🥇', '🌝', '🔫', '🐱', '🐣', '🎧', '💟', '👹', '💍', '🍼', '💡', '😽', '🍊', '😨', '🍫', '🧢', '🤕', '🎼', '🐻', '📲', '👻', '🧚', '🌮', '🍭', '🐟', '🐸', '🐝', '🐈', '🔵', '😧', '🌄', '😾', '🤸', '📱', '🍇', '🌴', '🐢', '🌃', '👽', '🍌', '📺', '👐', '🔔', '🌅', '🦄', '🎥', '🍋', '🥚', '💲', '📚', '🐔', '🎸', '🥃', '😿', '🚗', '🌎', '🔊', '🦅', '🚿', '🦆', '🍉', '🍬', '🧸', '🍨', '📝', '🤚', '📩', '💵', '👼', '💭', '🌍', '👧', '🤜', '🍿', '🧿', '🏀', '🍏', '🌳', '🙉', '😦', '🤰', '🍹', '🍦', '🛑', '🧘', '🍔', '🍂', '🐒', '🍪', '🙀', '🍗', '🌠', '🎬', '🌵', '🍄', '🐐', '🍩', '🦁', '🙆', '📞', '👸', '🍅', '🐍', '👦', '💬', '🥤', '😼', '🌾', '🧀', '🎮', '🧠', '🌏', '🛌', '🔝', '🌉', '🤛', '🤒', '👗', '🌲', '🍜', '🐦', '🍯', '👮', '🏅', '🐼', '💄', '👺', '🎆', '🎨', '🍞', '🎇', '🦜', '🐑', '🐙', '🦍', '🔗', '📖', '🔹', '🥓', '🥒', '🍸', '🥧', '💻', '🐖', '📈', '💊', '👩', '🌀', '💆', '🥩', '🎄', '🌽', '🤥', '🐎', '🆘', '💏', '🥕', '🔮', '🦀', '🐠', '🌛', '👠', '🐓', '🥊', '🛐', '🚬', '🔰', '🌜', '🍴', '🥔', '🎓', '👙', '🗿', '🥑', '👯', '🍍', '🏁', '👂', '🦊', '👃', '🦖', '🐴', '🎃', '🦠', '🌕', '📦', '🌌', '🍧', '🍟', '🎹', '🥞', '👣', '🥜', '🍡', '🦷', '🚴', '🍝', '🎻', '🐊', '🍖', '🐺', '🐽', '🚮', '🍵', '🌭', '🐄', '🥁', '🍳', '👫', '🔆', '🐳', '🌯', '🦴', '🥪', '🦃', '🎣', '🔻', '🐀', '🐬', '🍚', '🤖', '🐧', '🦈', '🏄', '🏈', '🧬', '🌐', '🔍', '📴', '🥦', '🐯', '📮', '🥛', '🥭', '🖖', '🐛', '🦞', '🐤', '🧟', '🍤', '🦐', '🎭', '🐞', '🐵', '🍣', '🥗', '🆔', '🔑', '👴', '🤴', '👵', '🤳', '🧨', '👤', '🎩', '🔙', '🥫', '🆕', '🥐', '👰', '💳', '🐚', '🌆', '🆗', '🤱', '👭', '🦇', '👨', '🦗', '🦕', '🏹', '🐮', '🚲', '💑']
    # fmt: on

    random.seed("chiffoncake")
    remo = lambda: random.choice(all_emojis)

    # fmt: off
    readers = (
        CardReader(id='s1', name='s1', type=CardReaderType.SPONSOR, time_emoji=[(datetime.min, remo())] + [(datetime(2023, 8, 18, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)] + [(datetime(2023, 8, 19, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)]),
        CardReader(id='s2', name='s2', type=CardReaderType.SPONSOR, time_emoji=[(datetime.min, remo())] + [(datetime(2023, 8, 18, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)] + [(datetime(2023, 8, 19, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)]),
        CardReader(id='s3', name='s3', type=CardReaderType.SPONSOR, time_emoji=[(datetime.min, remo())] + [(datetime(2023, 8, 18, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)] + [(datetime(2023, 8, 19, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)]),
        CardReader(id='s4', name='s4', type=CardReaderType.SPONSOR, time_emoji=[(datetime.min, remo())] + [(datetime(2023, 8, 18, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)] + [(datetime(2023, 8, 19, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)]),
        CardReader(id='s5', name='s5', type=CardReaderType.SPONSOR, time_emoji=[(datetime.min, remo())] + [(datetime(2023, 8, 18, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)] + [(datetime(2023, 8, 19, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)]),
        CardReader(id='s6', name='s6', type=CardReaderType.SPONSOR, time_emoji=[(datetime.min, remo())] + [(datetime(2023, 8, 18, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)] + [(datetime(2023, 8, 19, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)]),
        CardReader(id='s7', name='s7', type=CardReaderType.SPONSOR, time_emoji=[(datetime.min, remo())] + [(datetime(2023, 8, 18, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)] + [(datetime(2023, 8, 19, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)]),
        CardReader(id='s8', name='s8', type=CardReaderType.SPONSOR, time_emoji=[(datetime.min, remo())] + [(datetime(2023, 8, 18, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)] + [(datetime(2023, 8, 19, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)]),
        CardReader(id='s9', name='s9', type=CardReaderType.SPONSOR, time_emoji=[(datetime.min, remo())] + [(datetime(2023, 8, 18, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)] + [(datetime(2023, 8, 19, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)]),
        CardReader(id='s10', name='s10', type=CardReaderType.SPONSOR, time_emoji=[(datetime.min, remo())] + [(datetime(2023, 8, 18, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)] + [(datetime(2023, 8, 19, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)]),
        CardReader(id='s11', name='s11', type=CardReaderType.SPONSOR, time_emoji=[(datetime.min, remo())] + [(datetime(2023, 8, 18, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)] + [(datetime(2023, 8, 19, 9, 0, 0) + i * timedelta(minutes=10), remo()) for i in range(7 * 6)]),
        CardReader(id='sf1', name='sf1', type=CardReaderType.SPONSOR_FLUSH),
        CardReader(id='p1', name='p1', type=CardReaderType.POPCAT),
        CardReader(id='p2', name='p2', type=CardReaderType.POPCAT),
        CardReader(id='c1', name='c1', type=CardReaderType.CRYPTO),
        CardReader(id='c2', name='c2', type=CardReaderType.CRYPTO),
        CardReader(id='c3', name='c3', type=CardReaderType.CRYPTO),
        CardReader(id='c4', name='c4', type=CardReaderType.CRYPTO),
        CardReader(id='c5', name='c5', type=CardReaderType.CRYPTO),
        CardReader(id='d1', name='d1', type=CardReaderType.DINORUN),
    )
    # fmt: on
    return readers


async def handle_reader(db_: db.DB):
    for reader in gen_readers():
        await db_.write_reader(reader)


async def main():
    parser = argparse.ArgumentParser(
        description="Script to extract production info and create db."
    )

    parser.add_argument("uid_file", help="user uid file, one uid (hex) per line")

    args = parser.parse_args()

    uid_file = Path(args.uid_file)

    db.connect_db()
    db_ = await db.get_db()
    await db_.drop_all()

    await handle_uid_file(db_, uid_file)
    await handle_reader(db_)


if __name__ == "__main__":
    asyncio.run(main())
