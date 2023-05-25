from pathlib import Path
from typing import Annotated
from fastapi import Depends
from .db import DB, FilesystemDB


__db = None


def init_db():
    global __db
    __db = FilesystemDB(Path(".db"))


async def get_db() -> DB:
    return __db


DBDep = Annotated[DB, Depends(get_db)]
