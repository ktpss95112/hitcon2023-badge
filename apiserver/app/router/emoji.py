from fastapi import APIRouter, HTTPException

from ..dashboard import EmojiDict, dashboard
from ..dependency import DBDep
from ..model import EmojiRecord

router = APIRouter(
    prefix="/emoji",
    tags=["emoji"],
)


@router.get("/")
async def get_all_record(db: DBDep) -> list[EmojiRecord]:
    return await db.get_all_emoji()


@router.post("/force_push", tags=["dashboard"])
async def force_push_emoji_to_dashboard(db: DBDep) -> bool:
    if dashboard.disabled:
        raise HTTPException(500, "No dashboard available in server configuration")

    records = await db.get_all_emoji()
    return dashboard.batch_create_emojis(
        [
            EmojiDict(
                card_uid=record.card_uid, content=record.msg, timestamp=record.time
            )
            for record in records
        ]
    )
