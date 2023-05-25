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
