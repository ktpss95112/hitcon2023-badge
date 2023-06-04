from fastapi import APIRouter
from ..dependency import DBDep, GetUserDep
from ..model import User

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
