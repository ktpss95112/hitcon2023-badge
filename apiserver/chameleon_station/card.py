from .config import config


class Card:
    def __init__(self) -> None:
        # TODO: pyserial
        pass

    def read_all(self) -> bytes:
        # TODO
        data = b"ABCD".ljust(
            config.NUM_SECTOR * config.NUM_BLOCK * config.BLOCK_SIZE, b"\x00"
        )

        assert len(data) == config.NUM_SECTOR * config.NUM_BLOCK * config.BLOCK_SIZE
        return data

    def write_halfblock(self, data: bytes, start=0):
        assert len(data) == config.BLOCK_SIZE // 2
        assert start == 0 or start == config.BLOCK_SIZE
        # TODO


card = Card()
