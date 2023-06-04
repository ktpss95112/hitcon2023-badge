from datetime import datetime
import functools
from fastapi import APIRouter
from ..dependency import DBDep, GetUserDep, GetReaderDep, CheckCardReaderTypeDep
from ..model import User, CardReader, CardReaderType
from ..db import DB

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
async def tap_popcat(user: GetUserDep, reader: GetReaderDep, db: DBDep) -> bool:
    # TODO
    return True


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
    emoji_list = emoji_list[:10]  # TODO: configurable size of emoji_list

    # If the user simply wants to reset their emoji buffer, do not flush the content to dashboard.
    if not show:
        return True

    # TODO: push to frontend?
    print("received emoji:", repr(emoji_list), flush=True)

    return True
