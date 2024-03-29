from dataclasses import dataclass
from datetime import datetime


@dataclass
class Config:
    NUM_SECTOR = 16
    NUM_BLOCK = 4  # number of block per sector
    BLOCK_SIZE = 16  # number of byte per blocks
    DISPLAY_CHUNK = 4  # number of byte per chunk

    QRCODE_SIZE = 300

    WINDOW_WIDTH = 1600
    WINDOW_HEIGHT = 900
    PROGRESS_WINDOW_WIDTH = 400
    PROGRESS_WINDOW_HEIGHT = 100

    DEFAULT_FONT_SCALE = 1.2

    SERIAL_PORT = "/dev/ttyUSB0"
    SERIAL_BAUDRATE = 9600

    DAY1_START_TIME = datetime(2023, 8, 18, 0, 0, 0)
    DAY1_END_TIME = datetime(2023, 8, 19, 0, 0, 0)
    DAY2_START_TIME = datetime(2023, 8, 19, 0, 0, 0)
    DAY2_END_TIME = datetime(2023, 8, 20, 0, 0, 0)

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
    EMOJI_SIZE_CHUNK = (4, 2, 3)

    POPCAT_DAY1_CHUNK = (7, 0, 0)
    POPCAT_DAY2_CHUNK = (7, 0, 1)

    CRYPTO_NUM_CHUNK = (6, 0, 0)
    CRYPTO_HMAC_CHUNK = (
        (6, 1, 0), (6, 1, 1), (6, 1, 2), (6, 1, 3),
        (6, 2, 0), (6, 2, 1), (6, 2, 2), (6, 2, 3),
    )
    # fmt: on

    # TODO: add button in CommandFrame to flush emoji to dashboard
    FLUSH_EMOJI_ENABLED = True
    FLUSH_EMOJI_API = "http://localhost:5000/tap/sponsor_flush_emoji/sf1/user/"


config = Config()
