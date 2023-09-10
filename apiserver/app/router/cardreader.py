from datetime import datetime
from enum import Enum

from fastapi import APIRouter

from ..dependency import DBDep, GetReaderDep
from ..model import CardReader

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


class AvalibleDay(int, Enum):
    day1 = 1
    day2 = 2


class AvailablePart(int, Enum):
    part0 = 0
    part1 = 1
    part2 = 2
    part3 = 3


@router.get("/emoji_time_table/{reader_id}/day/{day}/part/{part}")
async def get_emoji_time_table_of_reader_with_day_and_part(
    reader: GetReaderDep, db: DBDep, day: AvalibleDay, part: AvailablePart
) -> list[tuple[datetime, str]]:
    """
    The returned list is composed of many items.
    Each item is composed of (start_time, emoji).
    """

    # TODO: more configurable
    day1_date = datetime(2023, 8, 18)
    day2_date = datetime(2023, 8, 19)

    if day == AvalibleDay.day1:
        all_emojis = [
            (dt, emoji)
            for dt, emoji in sorted(reader.time_emoji)
            if dt.year == day1_date.year
            and dt.month == day1_date.month
            and dt.day == day1_date.day
        ]
    elif day == AvalibleDay.day2:
        all_emojis = [
            (dt, emoji)
            for dt, emoji in sorted(reader.time_emoji)
            if dt.year == day2_date.year
            and dt.month == day2_date.month
            and dt.day == day2_date.day
        ]

    start = part * len(all_emojis) // 4
    end = (part + 1) * len(all_emojis) // 4
    return all_emojis[start:end]


@router.get("/{reader_id}")
async def get_reader(reader: GetReaderDep) -> CardReader:
    return reader


@router.post("/")
async def write_reader(reader: CardReader, db: DBDep):
    await db.write_reader(reader)
