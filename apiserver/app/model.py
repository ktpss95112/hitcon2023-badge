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
