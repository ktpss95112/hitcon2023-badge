from fastapi import APIRouter

from ..dependency import DBDep, GetUserDep
from ..model import PopcatRecord

router = APIRouter(
    prefix="/popcat",
    tags=["popcat"],
)


@router.get("/")
async def get_all_record(db: DBDep) -> list[PopcatRecord]:
    return await db.get_all_popcat()


@router.get("/score")
async def get_all_score(db: DBDep) -> dict[str, int]:
    """
    The returned object is the mapping of card_uid to score.
    All the records of user who has a popcat record will be returned.
    """
    return await db.get_all_popcat_score()


@router.get("/{card_uid}/score")
async def get_score(user: GetUserDep, db: DBDep) -> int:
    return await db.get_popcat_score_by_user(user)


@router.get("/{card_uid}/record")
async def get_record(user: GetUserDep, db: DBDep) -> list[PopcatRecord]:
    return await db.get_all_popcat_by_user(user)


# TODO: endpoint for force pushing data to dashboard
