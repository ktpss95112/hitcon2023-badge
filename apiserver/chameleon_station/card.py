import abc
import random
from collections import defaultdict

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

    def clear_emoji_buffer(self, data: bytes):
        """
        data: all the data on the card
        """
        assert len(data) == config.NUM_SECTOR * config.NUM_BLOCK * config.BLOCK_SIZE
        block_to_write = defaultdict(set)
        num_chunk = config.BLOCK_SIZE // config.DISPLAY_CHUNK

        # collect/merge the blocks
        block_to_write[config.EMOJI_SIZE_CHUNK[:2]].add(config.EMOJI_SIZE_CHUNK[2])
        for i_sector, i_block, i_chunk in config.EMOJI_CHUNKS:
            block_to_write[(i_sector, i_block)].add(i_chunk)

        # erase while persisting the data which should not be erased
        for (i_sector, i_block), (chunks) in block_to_write.items():
            data_to_write = [b"" for _ in range(num_chunk)]
            for i_chunk in range(num_chunk):
                start = (
                    i_sector * config.NUM_BLOCK + i_block
                ) * config.BLOCK_SIZE + i_chunk * config.DISPLAY_CHUNK
                end = start + config.DISPLAY_CHUNK
                chunk_data = data[start:end]

                if i_chunk in chunks:
                    data_to_write[i_chunk] = b"\x00" * config.DISPLAY_CHUNK
                else:
                    data_to_write[i_chunk] = chunk_data

            self.write_block(b"".join(data_to_write), i_sector, i_block)


class CardArduino(Card):
    def __init__(self, serial: pyserial.Serial):
        self.serial = serial

        self.__communicate(command=b"INIT\n", recv_start_with=b"I")

    def __consume_trailing_newline(self):
        self.serial.readline()

    def __communicate(
        self,
        command: bytes,
        recv_start_with: bytes,
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
            elif c == recv_start_with:
                return recv_callback()

    def read_block(self, i_block: int) -> bytes:
        def callback():
            content = self.serial.read(16)
            self.serial.readline()
            return content

        return self.__communicate(
            command=f"READ\n{i_block}\n".encode(),
            recv_start_with="O",
            recv_callback=callback,
        )

    def write_block(self, data: bytes, i_sector: int, i_block: int):
        assert len(data) == config.BLOCK_SIZE
        block_id = i_sector * config.NUM_BLOCK + i_block
        self.__communicate(
            command=f"WRITE\n{block_id}\n".encode() + data + b"\n", recv_start_with="O"
        )

    def write_uid(self, data: bytes):
        assert len(data) == 4
        self.__communicate(command=b"WRITE_UID\n" + data + b"\n", recv_start_with="O")

    def unbrick_card(self, data: bytes):
        assert len(data) == 4
        self.__communicate(command=b"UNBRICK\n" + data + b"\n", recv_start_with="O")

    def read_all(self) -> bytes:
        ret = b""
        for i_sector in range(config.NUM_SECTOR):
            for i_block in range(config.NUM_BLOCK):
                index = i_sector * config.NUM_BLOCK + i_block
                ret += self.read_block(index)
        return ret


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
    # TODO: a mock serial instead of a mock card, so that we can test whether CardArduino works correctly
    card: Card = CardMock()
