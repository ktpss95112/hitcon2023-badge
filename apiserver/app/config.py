import os
from dataclasses import dataclass
from typing import get_type_hints

from dotenv import load_dotenv


@dataclass
class Config:
    MONGODB_HOST: str = "localhost:27017"
    MONGODB_USERNAME: str = "root"
    MONGODB_PASSWORD: str = "example"
    MONGODB_DB_NAME: str = "badge"
    MONGODB_USER_TABLE_NAME: str = "user"
    MONGODB_CARE_READER_TABLE_NAME: str = "card-reader"
    MONGODB_POPCAT_RECORD_TABLE_NAME: str = "popcat-record"

    POPCAT_TAP_INTERVAL: int = 120

    SPONSOR_EMOJI_BUFFER_LENGTH: int = 10

    @classmethod
    def new(cls):
        config = cls()

        load_dotenv()

        for key in dir(cls):
            if key.startswith("__"):
                continue

            value = os.getenv(key)
            if (value is not None) and (value != ""):
                type_ = get_type_hints(cls)[key]
                setattr(config, key, type_(value))

        return config


config = Config.new()
