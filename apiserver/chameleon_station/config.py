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


config = Config()
