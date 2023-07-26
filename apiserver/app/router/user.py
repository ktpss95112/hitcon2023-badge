from fastapi import APIRouter

from ..dependency import DBDep, GetUserDep
from ..model import TapRecord, User

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


# TODO: check permission
@router.get("/{card_uid}")
async def read_user(user: GetUserDep) -> User:
    return user


# TODO: check permission
@router.post("/")
async def write_user(user: User, db: DBDep):
    await db.write_user(user)


# TODO: check permission
@router.get("/{card_uid}/tap_record", tags=["tap record"])
async def get_tap_record_by_user(user: GetUserDep, db: DBDep) -> list[TapRecord]:
    return await db.get_tap_record_by_user(user)
