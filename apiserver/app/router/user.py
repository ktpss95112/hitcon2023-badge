from datetime import datetime
from fastapi import APIRouter, HTTPException
from ..dependency import DBDep
from ..model import User

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


# TODO: check permission
@router.get("/{card_uid}")
async def read_user(card_uid: str, db: DBDep) -> User:
    user = await db.get_user_by_card_uid(card_uid)
    if user is None:
        raise HTTPException(404, "User not found.")
    return user


# TODO: check permission
@router.post("/")
async def write_user(user: User, db: DBDep):
    await db.write_user(user)


# TODO: check permission
# TODO: rate limit
@router.post("/{card_uid}/tap/{reader_id}")
async def card_tap_reader(card_uid: str, reader_id: str, db: DBDep) -> bool:
    user = await db.get_user_by_card_uid(card_uid)
    if user is None:
        raise HTTPException(404, "User not found.")

    reader = await db.get_reader_by_id(reader_id)
    if reader is None:
        raise HTTPException(404, "Card reader not found.")

    user.tap_record.append((datetime.now(), f"tapped {reader.id} ({reader.name})"))
    await db.write_user(user)

    # TODO: do different processing in background or call other callback functions?

    return True
