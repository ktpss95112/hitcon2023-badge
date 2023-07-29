import abc
import random

import serial as pyserial

from .config import config


class Card(abc.ABC):
    @abc.abstractmethod
    def read_all(self) -> bytes:
        pass

    @abc.abstractmethod
    def write_block(self, data: bytes, i_sector: int, i_block: int):
        pass

    @abc.abstractmethod
    def write_uid(self, data: bytes):
        pass

    @abc.abstractmethod
    def unbrick_card(self, data: bytes):
        pass


class CardArduino(Card):
    def __init__(self, serial: pyserial.Serial):
        self.serial = serial

        self.__communicate(command=b"INIT\n", recv_should_be=b"I")

    def __consume_trailing_newline(self):
        self.serial.readline()

    def __communicate(
        self,
        command: bytes,
        recv_should_be: bytes,
        recv_callback=__consume_trailing_newline,
    ):
        self.serial.write(command)
        while True:
            c = self.serial.read(1)
            if c == b"E":
                reason = self.serial.readline().strip()
                raise Exception(reason)
            elif c == b"D":
                msg = self.serial.readline().strip()
            elif c == recv_should_be:
                return recv_callback()

    def read_block(self, i_block: int) -> bytes:
        def callback():
            content = self.serial.read(16)
            self.serial.readline()
            return content

        return self.__communicate(
            command=f"READ\n{i_block}\n".encode(),
            recv_should_be="O",
            recv_callback=callback,
        )

    def write_block(self, data: bytes, i_sector: int, i_block: int):
        assert len(data) == config.BLOCK_SIZE
        block_id = i_sector * config.NUM_BLOCK + i_block
        self.__communicate(
            command=f"WRITE\n{block_id}\n".encode() + data + b"\n", recv_should_be="O"
        )

    def write_uid(self, data: bytes):
        assert len(data) == 4
        self.__communicate(command=b"WRITE_UID\n" + data + b"\n", recv_should_be="O")

    def unbrick_card(self, data: bytes):
        assert len(data) == 4
        self.__communicate(command=b"UNBRICK\n" + data + b"\n", recv_should_be="O")


class CardMock(Card):
    def __init__(self) -> None:
        self.data = random.randbytes(
            config.NUM_SECTOR * config.NUM_BLOCK * config.BLOCK_SIZE
        )

    def read_all(self) -> bytes:
        data = self.data

        assert len(data) == config.NUM_SECTOR * config.NUM_BLOCK * config.BLOCK_SIZE
        return data

    def write_block(self, data: bytes, i_sector: int, i_block: int):
        assert len(data) == config.BLOCK_SIZE
        start = (i_sector * config.NUM_BLOCK + i_block) * config.BLOCK_SIZE
        end = start + config.BLOCK_SIZE
        self.data = self.data[:start] + data + self.data[end:]

    def write_uid(self, data: bytes):
        assert len(data) == 4
        self.data = data + self.data[4:]

    def unbrick_card(self, data: bytes):
        self.write_uid(data)


try:
    serial = pyserial.Serial(config.SERIAL_PORT, config.SERIAL_BAUDRATE)
    card: Card = CardArduino(serial)
except:
    card: Card = CardMock()
