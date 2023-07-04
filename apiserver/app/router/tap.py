import functools
from datetime import datetime

from fastapi import APIRouter

from ..config import config
from ..db import DB
from ..dependency import CheckCardReaderTypeDep, DBDep, GetReaderDep, GetUserDep
from ..model import CardReader, CardReaderType, User

router = APIRouter(
    prefix="/tap",
    tags=["user card tap a card reader"],
)


def user_add_record(func):
    @functools.wraps(func)
    async def wrapper(user: User, reader: CardReader, db: DB, *args, **kwargs):
        ret = await func(user, reader, db, *args, **kwargs)
        user.add_record(datetime.now(), reader)
        await db.write_user(user)
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
)
@user_add_record
async def tap_popcat(
    user: GetUserDep, reader: GetReaderDep, db: DBDep, incr: int
) -> tuple[bool, int]:
    """
    The returned boolean indicates whether the submit is successful.
    The returned integer indicates the cooldown of the next tapping.
    """

    record = await db.get_popcat_by_card_uid(user)

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
    emoji_list: str,
    show: bool = True,
) -> bool:
    emoji_list = emoji_list[: config.SPONSOR_EMOJI_BUFFER_LENGTH]

    # If the user simply wants to reset their emoji buffer, do not flush the content to dashboard.
    if not show:
        return True

    # TODO: push to frontend?
    print("received emoji:", repr(emoji_list), flush=True)

    return True
