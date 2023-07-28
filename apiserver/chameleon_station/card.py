import random

from .config import config


class Card:
    def __init__(self) -> None:
        # TODO: pyserial
        self.data = random.randbytes(
            config.NUM_SECTOR * config.NUM_BLOCK * config.BLOCK_SIZE
        )

    def read_all(self) -> bytes:
        # TODO
        data = self.data

        assert len(data) == config.NUM_SECTOR * config.NUM_BLOCK * config.BLOCK_SIZE
        return data

    def write_block(self, data: bytes, i_sector: int, i_block: int):
        assert len(data) == config.BLOCK_SIZE
        # TODO
        start = (i_sector * config.NUM_BLOCK + i_block) * config.BLOCK_SIZE
        end = start + config.BLOCK_SIZE
        self.data = self.data[:start] + data + self.data[end:]


card = Card()
