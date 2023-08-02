from dataclasses import dataclass


@dataclass
class Config:
    NUM_SECTOR = 16
    NUM_BLOCK = 4  # number of block per sector
    BLOCK_SIZE = 16  # number of byte per blocks
    DISPLAY_CHUNK = 4  # number of byte per chunk

    QRCODE_SIZE = 300

    DEFAULT_FONT_SCALE = 1.2

    SERIAL_PORT = "/dev/ttyUSB0"
    SERIAL_BAUDRATE = 9600

    # fmt: off
    EMOJI_CHUNKS = ( # (i_sector, i_block, i_chunk)
        (0, 1, 0), (0, 1, 1), (0, 1, 2), (0, 1, 3),
        (0, 2, 0), (0, 2, 1), (0, 2, 2), (0, 2, 3),
        (1, 0, 0), (1, 0, 1), (1, 0, 2), (1, 0, 3),
        (1, 1, 0), (1, 1, 1), (1, 1, 2), (1, 1, 3),
        (1, 2, 0), (1, 2, 1), (1, 2, 2), (1, 2, 3),
        (2, 0, 0), (2, 0, 1), (2, 0, 2), (2, 0, 3),
        (2, 1, 0), (2, 1, 1), (2, 1, 2), (2, 1, 3),
        (2, 2, 0), (2, 2, 1), (2, 2, 2), (2, 2, 3),
        (3, 0, 0), (3, 0, 1), (3, 0, 2), (3, 0, 3),
        (3, 1, 0), (3, 1, 1), (3, 1, 2), (3, 1, 3),
        (3, 2, 0), (3, 2, 1), (3, 2, 2), (3, 2, 3),
        (4, 0, 0), (4, 0, 1), (4, 0, 2), (4, 0, 3),
        (4, 1, 0), (4, 1, 1), (4, 1, 2), (4, 1, 3),
        (4, 2, 0), (4, 2, 1), (4, 2, 2),
    )
    # fmt: on
    EMOJI_SIZE_CHUNK = (4, 2, 3)


config = Config()
