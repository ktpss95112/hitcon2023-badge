from dataclasses import dataclass
from enum import IntEnum


class UserType(IntEnum):
    STAFF_ADMIN = 0
    STAFF = 1
    ATTENDEE = 2


@dataclass
class User:
    name: str
    card_uid: str  # stores bytes.hex()
    type: UserType = UserType.ATTENDEE
