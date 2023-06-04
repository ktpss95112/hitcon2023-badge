from fastapi import APIRouter
from ..dependency import GetReaderDep, DBDep
from ..model import CardReader

router = APIRouter(
    prefix="/cardreader",
    tags=["card reader"],
)


# TODO: check permission
@router.get("/{reader_id}")
async def get_reader(reader: GetReaderDep) -> CardReader:
    return reader


# TODO: check permission
@router.post("/")
async def write_reader(reader: CardReader, db: DBDep):
    await db.write_reader(reader)
