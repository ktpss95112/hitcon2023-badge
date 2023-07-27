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


class PopcatRecord(BaseModel):
    card_uid: str
    time: datetime
    incr: int


# TODO: Do not use card_uid as primary key. Store every record separately. See class PopcatRecord.
class DinorunRecord(BaseModel):
    card_uid: str
    record: list[
        tuple[datetime, float]
    ] = []  # every item is the submission time and the score

    def add_record(self, time: datetime, score: float):
        self.record.append((time, score))

    def get_best_score(self) -> float:
        return max((score for time, score in self.record), default=0)
