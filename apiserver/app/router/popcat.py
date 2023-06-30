from fastapi import APIRouter

from ..dependency import DBDep, GetPopcatDep

router = APIRouter(
    prefix="/popcat",
    tags=["popcat"],
)


@router.get("/")
async def get_all(db: DBDep) -> dict[str, int]:
    """
    The returned object is the mapping of card_uid to score.
    All the records of user who has a popcat record will be returned.
    """
    all_record = await db.get_all_popcat()
    ret = {record.card_uid: record.get_score() for record in all_record}
    return ret


@router.get("/{card_uid}")
async def get_score(record: GetPopcatDep) -> int:
    return record.get_score()
