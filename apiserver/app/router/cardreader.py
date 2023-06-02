from fastapi import APIRouter, HTTPException
from ..dependency import DBDep
from ..model import CardReader

router = APIRouter(
    prefix="/cardreader",
    tags=["card reader"],
)


# TODO: check permission
@router.get("/{reader_id}")
async def get_reader(reader_id: str, db: DBDep) -> CardReader:
    reader = await db.get_reader_by_id(reader_id)
    if reader is None:
        raise HTTPException(404, "Card reader not found.")
    return reader


# TODO: check permission
@router.post("/")
async def write_reader(reader: CardReader, db: DBDep):
    await db.write_reader(reader)
