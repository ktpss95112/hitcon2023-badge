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
    tap_record: list[
        tuple[datetime, str]
    ] = []  # every item is a time along with a description

    # TODO: move the tap_record outside the class and make a new class TapRecord
    def add_record(self, time: datetime, reader: "CardReader"):
        self.tap_record.append((datetime.now(), f"tapped {reader.id} ({reader.name})"))


class CardReaderType(IntEnum):
    STAFF = 0
    SPONSOR = 1
    POPCAT = 2  # TODO: popcat game
    SPONSOR_FLUSH = 3


# Note: if create new columns, give an initial value as auto migration
class CardReader(BaseModel):
    id: str
    name: str
    type: CardReaderType
    time_emoji: list[
        tuple[datetime, str]
    ] = []  # every item is the start time along with the emoji


class PopcatRecord(BaseModel):
    card_uid: str
    record: list[
        tuple[datetime, int]
    ] = []  # every item is the tap time and the increment of his score

    def add_record(self, time: datetime, incr: int):
        self.record.append((time, incr))

    def get_score(self) -> int:
        # TODO: maybe sum the records which lie within a specific time interval
        return sum(incr for time, incr in self.record)
