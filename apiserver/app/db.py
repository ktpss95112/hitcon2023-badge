import abc
import atexit
import functools
import sys
from datetime import datetime
from pathlib import Path
from typing import Callable
from urllib.parse import quote_plus

import aiofiles
from pydantic import BaseModel
from pymongo import MongoClient

from .config import config
from .model import CardReader, DinorunRecord, PopcatRecord, TapRecord, User


class DB(abc.ABC):
    @abc.abstractmethod
    async def drop_all(self):
        pass

    @abc.abstractmethod
    async def get_user_by_card_uid(self, card_uid: str) -> User | None:
        pass

    @abc.abstractmethod
    async def write_user(self, user: User):
        pass

    @abc.abstractmethod
    async def get_reader_by_id(self, reader_id: str) -> CardReader | None:
        pass

    @abc.abstractmethod
    async def write_reader(self, reader: CardReader):
        pass

    @abc.abstractmethod
    async def get_all_reader(self) -> list[CardReader]:
        pass

    @abc.abstractmethod
    async def new_popcat(self, record: PopcatRecord):
        pass

    @abc.abstractmethod
    async def get_popcat_score_by_user(self, user: User) -> int:
        pass

    @abc.abstractmethod
    async def get_all_popcat_score(self) -> dict[str, int]:
        pass

    @abc.abstractmethod
    async def get_latest_popcat_time_by_user(self, user: User) -> PopcatRecord:
        pass

    @abc.abstractmethod
    async def get_all_popcat_by_user(self, user: User) -> list[PopcatRecord]:
        pass

    @abc.abstractmethod
    async def get_all_popcat(self) -> list[PopcatRecord]:
        pass

    @abc.abstractmethod
    async def del_all_popcat(self):
        pass

    @abc.abstractmethod
    async def new_dinorun(self, record: DinorunRecord):
        pass

    @abc.abstractmethod
    async def get_dinorun_score_by_user(self, user: User) -> float:
        pass

    @abc.abstractmethod
    async def get_all_dinorun_score(self) -> dict[str, float]:
        pass

    @abc.abstractmethod
    async def get_all_dinorun_by_user(self, user: User) -> list[DinorunRecord]:
        pass

    @abc.abstractmethod
    async def get_all_dinorun(self) -> list[DinorunRecord]:
        pass

    @abc.abstractmethod
    async def del_all_dinorun(self):
        pass

    @abc.abstractmethod
    async def new_tap_record(self, record: TapRecord):
        pass

    @abc.abstractmethod
    async def get_all_tap_record(self) -> list[TapRecord]:
        pass

    @abc.abstractmethod
    async def get_tap_record_by_user(self, user: User) -> list[TapRecord]:
        pass

    @abc.abstractmethod
    async def get_tap_record_by_reader(self, reader: CardReader) -> list[TapRecord]:
        pass


class MongoDB(DB):
    def __init__(self, client: MongoClient) -> None:
        self.__client = client

        self.__db = self.__client[config.MONGODB_DB_NAME]
        self.__user_table = self.__db[config.MONGODB_USER_TABLE_NAME]
        self.__tap_record_table = self.__db[config.MONGODB_TAP_RECORD_TABLE_NAME]
        self.__card_reader_table = self.__db[config.MONGODB_CARE_READER_TABLE_NAME]
        self.__popcat_record_table = self.__db[config.MONGODB_POPCAT_RECORD_TABLE_NAME]
        self.__dinorun_record_table = self.__db[
            config.MONGODB_DINORUN_RECORD_TABLE_NAME
        ]

        self.__all_collections = [
            self.__user_table,
            self.__tap_record_table,
            self.__card_reader_table,
            self.__popcat_record_table,
            self.__dinorun_record_table,
        ]

    async def drop_all(self):
        for collection in self.__all_collections:
            collection.drop()

    async def get_user_by_card_uid(self, card_uid: str) -> User | None:
        obj = self.__user_table.find_one({"card_uid": card_uid})
        if obj is None:
            return None
        return User.parse_obj(obj)

    async def write_user(self, user: User):
        self.__user_table.replace_one(
            {"card_uid": user.card_uid}, dict(user), upsert=True
        )

    async def get_reader_by_id(self, reader_id: str) -> CardReader | None:
        obj = self.__card_reader_table.find_one({"id": reader_id})
        if obj is None:
            return None
        return CardReader.parse_obj(obj)

    async def write_reader(self, reader: CardReader):
        self.__card_reader_table.replace_one(
            {"id": reader.id}, dict(reader), upsert=True
        )

    async def get_all_reader(self) -> list[CardReader]:
        return [CardReader.parse_obj(obj) for obj in self.__card_reader_table.find()]

    async def new_popcat(self, record: PopcatRecord):
        self.__popcat_record_table.insert_one(dict(record))

    async def get_popcat_score_by_user(self, user: User) -> int:
        # TODO: optimize?
        tmp = await self.get_all_popcat_score()
        return tmp.get(user.card_uid, 0)

    async def get_all_popcat_score(self) -> dict[str, int]:
        """
        The returned dictionary:
        * key: card_uid
        * value: score
        """
        tmp = self.__popcat_record_table.aggregate(
            [{"$group": {"_id": "$card_uid", "score": {"$sum": "$incr"}}}]
        )
        return {result["_id"]: result["score"] for result in tmp}

    async def get_latest_popcat_time_by_user(self, user: User) -> datetime:
        # TODO: optimize?
        tmp = await self.get_all_popcat_by_user(user)
        return max((record.time for record in tmp), default=datetime.min)

    async def get_all_popcat_by_user(self, user: User) -> list[PopcatRecord]:
        return list(
            map(
                PopcatRecord.parse_obj,
                self.__popcat_record_table.find({"card_uid": user.card_uid}),
            )
        )

    async def get_all_popcat(self) -> list[PopcatRecord]:
        return list(map(PopcatRecord.parse_obj, self.__popcat_record_table.find()))

    async def del_all_popcat(self):
        self.__popcat_record_table.drop()

    async def new_dinorun(self, record: DinorunRecord):
        self.__dinorun_record_table.insert_one(dict(record))

    async def get_dinorun_score_by_user(self, user: User) -> float:
        # TODO: optimize?
        tmp = await self.get_all_dinorun_score()
        return tmp.get(user.card_uid, 0)

    async def get_all_dinorun_score(self) -> dict[str, float]:
        """
        The returned dictionary:
        * key: card_uid
        * value: score
        """
        tmp = self.__dinorun_record_table.aggregate(
            [{"$group": {"_id": "$card_uid", "score": {"$max": "$score"}}}]
        )
        return {result["_id"]: result["score"] for result in tmp}

    async def get_all_dinorun_by_user(self, user: User) -> list[DinorunRecord]:
        return list(
            map(
                DinorunRecord.parse_obj,
                self.__dinorun_record_table.find({"card_uid": user.card_uid}),
            )
        )

    async def get_all_dinorun(self) -> list[DinorunRecord]:
        return list(map(DinorunRecord.parse_obj, self.__dinorun_record_table.find()))

    async def del_all_dinorun(self):
        self.__dinorun_record_table.drop()

    async def new_tap_record(self, record: TapRecord):
        self.__tap_record_table.insert_one(dict(record))

    async def get_all_tap_record(self) -> list[TapRecord]:
        return list(map(TapRecord.parse_obj, self.__tap_record_table.find()))

    async def get_tap_record_by_user(self, user: User) -> list[TapRecord]:
        return list(
            map(
                TapRecord.parse_obj,
                self.__tap_record_table.find({"card_uid": user.card_uid}),
            )
        )

    async def get_tap_record_by_reader(self, reader: CardReader) -> list[TapRecord]:
        return list(
            map(
                TapRecord.parse_obj,
                self.__tap_record_table.find({"reader_id": reader.id}),
            )
        )


# class FilesystemDB(DB):
#     def __init__(self, path: Path):
#         if not path.exists():
#             path.mkdir()
#         assert path.is_dir(), f"{path} is not a directory"
#         self.path = path

#     def get_filename_from_card_uid(self, card_uid: str):
#         return self.path / f"user-{card_uid}.json"

#     def get_filename_from_reader_id(self, reader_id: str):
#         return self.path / f"reader-{reader_id}.json"

#     def get_filename_for_popcat(self, card_uid: str):
#         return self.path / f"popcat-{card_uid}.json"

#     async def default_read(self, model_type: BaseModel, index_to_path: Callable, index):
#         filename = index_to_path(self, index)
#         if not filename.exists():
#             return None
#         async with aiofiles.open(filename, "r") as f:
#             return model_type.parse_raw(await f.read())

#     async def get_obj_from_path(self, file: Path, type_: BaseModel):
#         async with aiofiles.open(file, "r") as f:
#             return type_.parse_raw(await f.read())

#     async def default_write(
#         self, index_to_path: Callable, obj_to_index: Callable, obj: BaseModel
#     ):
#         index = obj_to_index(obj)
#         filename = index_to_path(self, index)
#         async with aiofiles.open(filename, "w") as f:
#             await f.write(obj.json())

#     get_user_by_card_uid = functools.partialmethod(
#         default_read, User, get_filename_from_card_uid
#     )
#     write_user = functools.partialmethod(
#         default_write, get_filename_from_card_uid, lambda user: user.card_uid
#     )

#     get_reader_by_id = functools.partialmethod(
#         default_read, CardReader, get_filename_from_reader_id
#     )
#     write_reader = functools.partialmethod(
#         default_write, get_filename_from_reader_id, lambda reader: reader.id
#     )

#     async def get_popcat_by_user(self, user: User) -> PopcatRecord:
#         ret = await self.default_read(
#             PopcatRecord, self.__class__.get_filename_for_popcat, user.card_uid
#         )
#         # If the record is not created before, create it.
#         if ret is None:
#             ret = PopcatRecord(card_uid=user.card_uid)
#         return ret

#     write_popcat = functools.partialmethod(
#         default_write, get_filename_for_popcat, lambda record: record.card_uid
#     )

#     async def get_all_reader(self) -> list[CardReader]:
#         return [
#             await self.get_obj_from_path(file, CardReader)
#             for file in self.path.iterdir()
#             if file.name.startswith("reader-")
#         ]

#     async def get_all_popcat(self) -> list[PopcatRecord]:
#         return [
#             await self.get_obj_from_path(file, PopcatRecord)
#             for file in self.path.iterdir()
#             if file.name.startswith("popcat-")
#         ]


__db = None


def __new_mongodb() -> MongoDB:
    client = MongoClient(
        config.MONGODB_HOST,
        username=config.MONGODB_USERNAME,
        password=config.MONGODB_PASSWORD,
    )

    return MongoDB(client=client)


def connect_db():
    global __db
    __db = __new_mongodb()


async def get_db() -> DB:
    return __db
