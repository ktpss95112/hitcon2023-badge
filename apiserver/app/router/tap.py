import functools
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body

from ..config import config
from ..db import DB
from ..dependency import CheckCardReaderTypeDep, DBDep, GetReaderDep, GetUserDep
from ..model import (
    CardReader,
    CardReaderType,
    EmojiRecord,
    PopcatRecord,
    TapRecord,
    User,
)

router = APIRouter(
    prefix="/tap",
    tags=["user card tap a card reader"],
)


def user_add_record(func):
    """
    The wrapped function should have `user, reader, db` as the first 3 arguments.
    """

    @functools.wraps(func)
    async def wrapper(user: User, reader: CardReader, db: DB, *args, **kwargs):
        ret = await func(user, reader, db, *args, **kwargs)
        await db.new_tap_record(
            TapRecord(card_uid=user.card_uid, reader_id=reader.id, time=datetime.now())
        )
        return ret

    return wrapper


@router.post(
    "/sponsor/{reader_id}/user/{card_uid}",
    dependencies=[CheckCardReaderTypeDep(CardReaderType.SPONSOR)],
    tags=["emoji"],
)
@user_add_record
async def tap_sponsor(user: GetUserDep, reader: GetReaderDep, db: DBDep) -> bool:
    return True


@router.post(
    "/popcat/{reader_id}/user/{card_uid}",
    dependencies=[CheckCardReaderTypeDep(CardReaderType.POPCAT)],
    tags=["popcat"],
)
@user_add_record
async def tap_popcat(
    user: GetUserDep,
    reader: GetReaderDep,
    db: DBDep,
    incr: int,
) -> tuple[bool, int]:
    """
    The returned boolean indicates whether the submission is successful.
    The returned integer indicates the cooldown of the next tapping.
    """

    # check whether the user taps too fast
    COOLDOWN = config.POPCAT_TAP_INTERVAL
    last_time = await db.get_latest_popcat_time_by_user(user)
    now = datetime.now()
    cooldown = COOLDOWN - int((now - last_time).total_seconds())
    if cooldown > 0:
        return False, cooldown

    # be aware that the validity of incr is not checked
    await db.new_popcat(
        PopcatRecord(card_uid=user.card_uid, time=datetime.now(), incr=incr)
    )

    return True, COOLDOWN


@router.post(
    "/sponsor_flush_emoji/{reader_id}/user/{card_uid}",
    dependencies=[CheckCardReaderTypeDep(CardReaderType.SPONSOR_FLUSH)],
    tags=["emoji"],
)
@user_add_record
async def tap_sponsor_flush_emoji(
    user: GetUserDep,
    reader: GetReaderDep,
    db: DBDep,
    emoji_list: Annotated[str, Body()],
    show: Annotated[bool, Body()] = True,
) -> bool:
    """
    If the user simply wants to reset their emoji buffer, do not flush the content to dashboard.
    In that case, `show` should be set to False.
    """

    emoji_list = emoji_list[: config.SPONSOR_EMOJI_BUFFER_LENGTH]

    if not show:
        return True

    await db.new_emoji(
        EmojiRecord(card_uid=user.card_uid, time=datetime.now(), msg=emoji_list)
    )

    return True


@router.post(
    "/crypto/{reader_id}/user/{card_uid}",
    dependencies=[
        CheckCardReaderTypeDep(CardReaderType.SPONSOR, CardReaderType.CRYPTO)
    ],  # TODO: sponsor reader has the functionality only works under the settings of HITCON 2023. Change the schema of reader so that reader.type holds a list instead of a single type.
    tags=["crypto"],
)
@user_add_record
async def tap_crypto(user: GetUserDep, reader: GetReaderDep, db: DBDep) -> bool:
    return True


@router.get("/tap_record", tags=["tap record"])
async def get_all_tap_record(db: DBDep) -> list[TapRecord]:
    return await db.get_all_tap_record()


@router.get("/tap_record/user/{card_uid}", tags=["tap record"])
async def get_tap_record_by_user(user: GetUserDep, db: DBDep) -> list[TapRecord]:
    return await db.get_tap_record_by_user(user)


@router.get("/tap_record/cardreader/{reader_id}", tags=["tap record"])
async def get_tap_record_by_reader(reader: GetReaderDep, db: DBDep) -> list[TapRecord]:
    return await db.get_tap_record_by_reader(reader)


@router.get("/tap_record/user/{card_uid}/cardreader/{reader_id}", tags=["tap record"])
async def get_tap_record_by_user(
    user: GetUserDep, reader: GetReaderDep, db: DBDep
) -> list[TapRecord]:
    return await db.get_tap_record_by_user_and_reader(user, reader)
