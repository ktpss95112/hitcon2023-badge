from fastapi import APIRouter, HTTPException

from ..dependency import DBDep
from ..model import EmojiRecord

router = APIRouter(
    prefix="/emoji",
    tags=["emoji"],
)


@router.get("/")
async def get_all_record(db: DBDep) -> list[EmojiRecord]:
    return await db.get_all_emoji()
