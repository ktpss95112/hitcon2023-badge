from datetime import datetime
from enum import IntEnum
from typing import List, Tuple
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
    tap_record: List[
        Tuple[datetime, str]
    ] = []  # every item is a time along with a description

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
    time_emoji: List[
        Tuple[datetime, str]
    ] = []  # every item is the start time along with the emoji
