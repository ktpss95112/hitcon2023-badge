import abc
import atexit
import functools
import sys
from pathlib import Path
from typing import Callable

import aiofiles
import docker
import docker.errors
from pydantic import BaseModel

from .model import CardReader, PopcatRecord, User


class DB(abc.ABC):
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
    async def get_popcat_by_card_uid(self, user: User) -> PopcatRecord:
        pass

    @abc.abstractmethod
    async def write_popcat(self, record: PopcatRecord):
        pass

    @abc.abstractmethod
    async def get_all_popcat(self) -> list[PopcatRecord]:
        pass


class MongoDB(DB):
    pass


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

#     async def get_popcat_by_card_uid(self, user: User) -> PopcatRecord:
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
    # TODO: configurable connection info
    # TODO: remote connection

    # currently only support local docker MongoDB
    client = docker.from_env()
    container_name = "apiserver-mongodb"
    image_name = "mongo"
    image_tag = "6.0.6"
    try:
        container = client.containers.get(container_name)
    except docker.errors.NotFound:
        print("mongo image not found, pulling and creating ...", file=sys.stderr)
        client.images.pull(image_name, image_tag)
        container = client.containers.create(
            f"{image_name}:{image_tag}", ports={27017: 27017}
        )
        container.rename(container_name)

    container.start()
    atexit.register(container.stop)

    return MongoDB()


def init_db():
    global __db
    __db = __new_mongodb()


async def get_db() -> DB:
    return __db
