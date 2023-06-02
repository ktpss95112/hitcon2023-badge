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
        raise HTTPException(404)
    return user


# TODO: check permission
@router.post("/")
async def write_user(user: User, db: DBDep):
    await db.write_user(user)
