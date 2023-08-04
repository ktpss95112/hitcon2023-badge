import abc
import io
import random
from collections import defaultdict, deque

import serial as pyserial

from .config import config


class SerialBase(abc.ABC):
    @abc.abstractmethod
    def readline(self) -> bytes:
        pass

    @abc.abstractmethod
    def read(self, size) -> bytes:
        pass

    @abc.abstractmethod
    def write(self, buf) -> int:
        pass


class ArduinoSerialMock(SerialBase):
    def __init__(self):
        self.data = b""
        self.output_buf = deque()

    def write(self, buf: bytes) -> bytes:
        input_buf = io.BytesIO(buf)
        while True:
            line = input_buf.readline()
            if line == b"":
                break

            elif line == b"INIT\n":
                self.data = random.randbytes(
                    config.NUM_SECTOR * config.NUM_BLOCK * config.BLOCK_SIZE
                )
                self.output_buf.extend(b"I\n")

            elif line == b"READ\n":
                block_id = int(input_buf.readline())
                start = block_id * config.BLOCK_SIZE
                end = start + config.BLOCK_SIZE
                data = self.data[start:end]
                self.output_buf.extend(b"O" + data + b"\n")

            elif line == b"WRITE\n":
                block_id = int(input_buf.readline())
                start = block_id * config.BLOCK_SIZE
                end = start + config.BLOCK_SIZE
                data = input_buf.read(config.BLOCK_SIZE + 1)[: config.BLOCK_SIZE]
                self.data = self.data[:start] + data + self.data[end:]
                self.output_buf.extend(b"O\n")

            elif line == b"WRITE_UID\n":
                new_uid = input_buf.read(5)[:4]
                self.data = new_uid + self.data[4:]
                self.output_buf.extend(b"O\n")

            elif line == b"UNBRICK\n":
                new_uid = input_buf.read(5)[:4]
                self.data = new_uid + self.data[4:]
                self.output_buf.extend(b"O\n")

    def read(self, size) -> bytes:
        ret = bytearray()
        for _ in range(size):
            try:
                ret.append(self.output_buf.popleft())
            except IndexError:
                break
        return bytes(ret)

    def readline(self) -> bytes:
        ret = bytearray()
        while True:
            try:
                ret.append(self.output_buf.popleft())
            except IndexError:
                break
            if ret[-1] == ord("\n"):
                break
        return bytes(ret)


class CardArduino:
    def __init__(self, serial: SerialBase):
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
                reason = self.serial.readline().rstrip()
                raise Exception(reason)
            elif c == b"D":
                msg = self.serial.readline().rstrip()
            elif c == recv_start_with:
                return recv_callback(self)

    def read_block(self, i_block: int) -> bytes:
        def callback(*args):
            content = self.serial.read(16)
            self.serial.readline()
            return content

        return self.__communicate(
            command=f"READ\n{i_block}\n".encode(),
            recv_start_with=b"O",
            recv_callback=callback,
        )

    def write_block(self, data: bytes, i_sector: int, i_block: int):
        assert len(data) == config.BLOCK_SIZE
        block_id = i_sector * config.NUM_BLOCK + i_block
        self.__communicate(
            command=f"WRITE\n{block_id}\n".encode() + data + b"\n", recv_start_with=b"O"
        )

    def write_uid(self, data: bytes):
        assert len(data) == 4
        self.__communicate(command=b"WRITE_UID\n" + data + b"\n", recv_start_with=b"O")

    def unbrick_card(self, data: bytes):
        assert len(data) == 4
        self.__communicate(command=b"UNBRICK\n" + data + b"\n", recv_start_with=b"O")

    def read_all(self) -> bytes:
        ret = b""
        for i_sector in range(config.NUM_SECTOR):
            for i_block in range(config.NUM_BLOCK):
                index = i_sector * config.NUM_BLOCK + i_block
                ret += self.read_block(index)
        return ret

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


try:
    serial = pyserial.Serial(config.SERIAL_PORT, config.SERIAL_BAUDRATE)
except:
    serial = ArduinoSerialMock()

card = CardArduino(serial)
