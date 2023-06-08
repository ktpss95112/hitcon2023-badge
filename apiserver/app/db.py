import abc
import functools
from pathlib import Path
from typing import Callable, List

import aiofiles
from pydantic import BaseModel

from .model import CardReader, User


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
    async def get_all_reader(self) -> List[CardReader]:
        pass


# TODO (maybe won't do it)
# class MongoDB(DB):
#     pass


class FilesystemDB(DB):
    def __init__(self, path: Path):
        if not path.exists():
            path.mkdir()
        assert path.is_dir(), f"{path} is not a directory"
        self.path = path

    def get_filename_from_card_uid(self, card_uid):
        return self.path / f"user-{card_uid}.json"

    def get_filename_from_reader_id(self, reader_id):
        return self.path / f"reader-{reader_id}.json"

    async def default_read(self, model_type: BaseModel, index_to_path: Callable, index):
        filename = index_to_path(self, index)
        if not filename.exists():
            return None
        async with aiofiles.open(filename, "r") as f:
            return model_type.parse_raw(await f.read())

    async def get_reader_from_path(self, file: Path) -> CardReader:
        async with aiofiles.open(file, "r") as f:
            return CardReader.parse_raw(await f.read())

    async def default_write(
        self, index_to_path: Callable, obj_to_index: Callable, obj: BaseModel
    ):
        index = obj_to_index(obj)
        filename = index_to_path(self, index)
        async with aiofiles.open(filename, "w") as f:
            await f.write(obj.json())

    get_user_by_card_uid = functools.partialmethod(
        default_read, User, get_filename_from_card_uid
    )
    write_user = functools.partialmethod(
        default_write, get_filename_from_card_uid, lambda user: user.card_uid
    )

    get_reader_by_id = functools.partialmethod(
        default_read, CardReader, get_filename_from_reader_id
    )
    write_reader = functools.partialmethod(
        default_write, get_filename_from_reader_id, lambda reader: reader.id
    )

    async def get_all_reader(self) -> List[CardReader]:
        return [
            await self.get_reader_from_path(file)
            for file in self.path.iterdir()
            if file.name.startswith("reader-")
        ]


__db = None


def init_db():
    global __db
    __db = FilesystemDB(Path(".db"))


async def get_db() -> DB:
    return __db
