import abc
from .model import User


class DB(abc.ABC):
    @abc.abstractmethod
    def get_user_by_card_uid(self, card_uid) -> User:
        pass

    @abc.abstractmethod
    def write_user(self, user: User):
        pass


# TODO (maybe won't do it)
# class MongoDB(DB):
#     pass


# TODO:
# class FilesystemDB(DB):
#     pass
