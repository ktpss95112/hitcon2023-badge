from dataclasses import dataclass


@dataclass
class Config:
    NUM_SECTOR = 16
    NUM_BLOCK = 4  # number of block per sector
    BLOCK_SIZE = 16  # number of byte per blocks

    QRCODE_SIZE = 300


config = Config()
