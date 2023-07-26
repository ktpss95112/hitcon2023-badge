from datetime import datetime

from fastapi import APIRouter

from ..dependency import DBDep, GetReaderDep
from ..model import CardReader, TapRecord

router = APIRouter(
    prefix="/cardreader",
    tags=["card reader"],
)


@router.get("/emoji_time_table")
async def get_emoji_time_table(db: DBDep) -> list[tuple[str, datetime, str]]:
    """
    The returned list is composed of many items.
    Each item is composed of (reader_id, start_time, emoji).
    """
    reader_list = await db.get_all_reader()
    return [
        (reader.id, dt, emoji)
        for reader in reader_list
        for dt, emoji in sorted(reader.time_emoji)
    ]


@router.get("/emoji_time_table/{reader_id}")
async def get_emoji_time_table_of_reader(
    reader: GetReaderDep, db: DBDep
) -> list[tuple[datetime, str]]:
    """
    The returned list is composed of many items.
    Each item is composed of (start_time, emoji).
    """
    return [(dt, emoji) for dt, emoji in sorted(reader.time_emoji)]


# TODO: check permission
@router.get("/{reader_id}")
async def get_reader(reader: GetReaderDep) -> CardReader:
    return reader


# TODO: check permission
@router.post("/")
async def write_reader(reader: CardReader, db: DBDep):
    await db.write_reader(reader)


# TODO: check permission
@router.get("/{reader_id}/tap_record", tags=["tap record"])
async def get_tap_record_by_user(reader: GetReaderDep, db: DBDep) -> list[TapRecord]:
    return await db.get_tap_record_by_reader(reader)
