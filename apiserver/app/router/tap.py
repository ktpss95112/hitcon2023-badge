import functools
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body

from ..config import config
from ..db import DB
from ..dependency import (
    CheckCardReaderTypeDep,
    DBDep,
    GetPopcatDep,
    GetReaderDep,
    GetUserDep,
)
from ..model import CardReader, CardReaderType, TapRecord, User

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
    user: GetUserDep, reader: GetReaderDep, db: DBDep, record: GetPopcatDep, incr: int
) -> tuple[bool, int]:
    """
    The returned boolean indicates whether the submission is successful.
    The returned integer indicates the cooldown of the next tapping.
    """

    # check whether the user taps too fast
    COOLDOWN = config.POPCAT_TAP_INTERVAL
    now = datetime.now()
    cooldown = (
        COOLDOWN - int((now - max(record.record)[0]).total_seconds())
        if record.record
        else 0
    )
    if cooldown > 0:
        return False, cooldown

    # TODO: be aware that the validity of incr is not checked
    record.add_record(datetime.now(), incr)
    await db.write_popcat(record)

    return True, COOLDOWN


@router.post(
    "/sponsor_flush_emoji/{reader_id}/user/{card_uid}",
    dependencies=[CheckCardReaderTypeDep(CardReaderType.SPONSOR_FLUSH)],
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

    # TODO: push to frontend?
    print("received emoji:", repr(emoji_list), flush=True)

    return True


@router.post(
    "/crypto/{reader_id}/user/{card_uid}",
    dependencies=[CheckCardReaderTypeDep(CardReaderType.CRYPTO)],
    tags=["crypto"],
)
@user_add_record
async def tap_crypto(user: GetUserDep, reader: GetReaderDep, db: DBDep) -> bool:
    return True
