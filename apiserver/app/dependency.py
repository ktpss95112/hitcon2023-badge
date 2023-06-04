from typing import Annotated
from fastapi import Depends, HTTPException
from .db import DB, get_db
from .model import User, CardReader, CardReaderType


DBDep = Annotated[DB, Depends(get_db)]


async def __get_user(card_uid: str, db: DBDep) -> User:
    user = await db.get_user_by_card_uid(card_uid)
    if user is None:
        raise HTTPException(404, "User not found.")
    return user


GetUserDep = Annotated[User, Depends(__get_user)]


async def __get_reader(reader_id: str, db: DBDep) -> CardReader:
    reader = await db.get_reader_by_id(reader_id)
    if reader is None:
        raise HTTPException(404, "Card reader not found.")
    return reader


GetReaderDep = Annotated[CardReader, Depends(__get_reader)]


class __CheckCardReaderType:
    def __init__(self, type: CardReaderType) -> None:
        self.type = type

    async def __call__(self, reader_id: str, db: DBDep):
        reader = await db.get_reader_by_id(reader_id)
        if reader is None:
            raise HTTPException(404, "Card reader not found.")
        if reader.type != self.type:
            raise HTTPException(403, "Invalid card reader")


CheckCardReaderTypeDep = lambda type: Depends(__CheckCardReaderType(type))
