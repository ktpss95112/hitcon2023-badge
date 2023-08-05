from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel


class UserType(IntEnum):
    STAFF_ADMIN = 0
    STAFF = 1
    ATTENDEE = 2


# Note: if create new columns, give an initial value as auto migration
class User(BaseModel):
    name: str
    card_uid: str  # stores bytes.hex()
    type: UserType = UserType.ATTENDEE

    def __hash__(self) -> int:
        return hash(f"user{self.card_uid}")


class TapRecord(BaseModel):
    card_uid: str
    reader_id: str
    time: datetime


class CardReaderType(IntEnum):
    STAFF = 0
    SPONSOR = 1
    POPCAT = 2
    SPONSOR_FLUSH = 3
    DINORUN = 4
    CRYPTO = 5


# Note: if create new columns, give an initial value as auto migration
class CardReader(BaseModel):
    id: str
    name: str
    type: CardReaderType
    time_emoji: list[
        tuple[datetime, str]
    ] = []  # every item is the start time along with the emoji

    def __hash__(self) -> int:
        return hash(f"reader{self.id}")


class EmojiRecord(BaseModel):
    card_uid: str
    time: datetime
    msg: str


class PopcatRecord(BaseModel):
    card_uid: str
    time: datetime
    incr: int


class DinorunRecord(BaseModel):
    card_uid: str
    time: datetime
    score: float


class ActivityDate(IntEnum):
    fisrt = 1
    second = 2


class CryptoRedeemRecord(BaseModel):
    card_uid: str
    date: ActivityDate
    time: datetime
