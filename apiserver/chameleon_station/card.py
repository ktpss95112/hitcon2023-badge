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

    def write_chunk(self, data: bytes, sector: int, block: int, chunk: int):
        assert len(data) == config.DISPLAY_CHUNK
        # TODO
        start = (
            sector * config.NUM_BLOCK + block
        ) * config.BLOCK_SIZE + chunk * config.DISPLAY_CHUNK
        end = start + config.DISPLAY_CHUNK
        self.data = self.data[:start] + data + self.data[end:]

    def write_halfblock(self, data: bytes, start=0):
        assert len(data) == config.BLOCK_SIZE // 2
        assert start == 0 or start == config.BLOCK_SIZE
        # TODO


card = Card()
