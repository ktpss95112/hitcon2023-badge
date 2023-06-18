from datetime import datetime
from typing import List, Tuple

from fastapi import APIRouter

from ..dependency import DBDep, GetReaderDep
from ..model import CardReader

router = APIRouter(
    prefix="/cardreader",
    tags=["card reader"],
)


@router.get("/emoji_time_table")
async def get_emoji_time_table(db: DBDep) -> List[Tuple[str, datetime, str]]:
    """
    The returned list is composed of many items.
    Each item is composed of (reader_id, start_time, emoji).
    """
    reader_list = await db.get_all_reader()
    return [
        (reader.id, dt, emoji)
        for reader in reader_list
        for dt, emoji in reader.time_emoji
    ]


@router.get("/emoji_time_table/{reader_id}")
async def get_emoji_time_table_of_reader(
    reader: GetReaderDep, db: DBDep
) -> List[Tuple[datetime, str]]:
    """
    The returned list is composed of many items.
    Each item is composed of (start_time, emoji).
    """
    return [(dt, emoji) for dt, emoji in reader.time_emoji]


# TODO: check permission
@router.get("/{reader_id}")
async def get_reader(reader: GetReaderDep) -> CardReader:
    return reader


# TODO: check permission
@router.post("/")
async def write_reader(reader: CardReader, db: DBDep):
    await db.write_reader(reader)
