import abc
from pathlib import Path
import aiofiles

from .model import User


class DB(abc.ABC):
    @abc.abstractmethod
    async def get_user_by_card_uid(self, card_uid: str) -> User | None:
        pass

    @abc.abstractmethod
    async def write_user(self, user: User):
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
        return self.path / f"{card_uid}.json"

    async def get_user_by_card_uid(self, card_uid: str) -> User:
        filename = self.get_filename_from_card_uid(card_uid)
        if not filename.exists():
            return None
        async with aiofiles.open(filename, "r") as f:
            return User.parse_raw(await f.read())

    async def write_user(self, user: User):
        filename = self.get_filename_from_card_uid(user.card_uid)
        async with aiofiles.open(filename, "w") as f:
            await f.write(user.json())
