from typing import Annotated

from fastapi import Depends, HTTPException

from .db import DB, get_db
from .model import CardReader, CardReaderType, DinorunRecord, PopcatRecord, User

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
    def __init__(self, *types: CardReaderType) -> None:
        self.types = types

    async def __call__(self, reader_id: str, db: DBDep):
        reader = await db.get_reader_by_id(reader_id)
        if reader is None:
            raise HTTPException(404, "Card reader not found.")
        if reader.type not in self.types:
            raise HTTPException(403, "Invalid card reader")


CheckCardReaderTypeDep = lambda *types: Depends(__CheckCardReaderType(*types))
