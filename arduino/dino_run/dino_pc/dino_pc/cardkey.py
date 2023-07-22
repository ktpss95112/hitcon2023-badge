import asyncio
from collections.abc import Callable

from dino_pc.aio_serial import SerialProtocol


def default_card_down_callback(uid: str):
    print(f"card down, uid={uid}")


def default_card_up_callback(uid: str):
    print(f"card up, uid={uid}")


class CardKey:
    def __init__(self, protocal: SerialProtocol) -> None:
        self.card_down_callback: Callable[[str], None] = default_card_down_callback
        self.card_up_callback: Callable[[str], None] = default_card_up_callback
        self.card_uid = None
        self._up_task: asyncio.Task = None

        @protocal.add_event_listener("data_received")
        def data_received_handler(data: bytes):
            uid = data.decode().splitlines()[-1][:8]
            if self._up_task is not None:
                self._up_task.cancel()
                self._up_task = None
            if uid != self.card_uid:
                if self.card_uid is not None:
                    self.card_up_callback(self.card_uid)
                self.card_uid = uid
                self.card_down_callback(uid)

            async def up_coro():
                # sleep time should be greater than arduino nfc reader interval
                await asyncio.sleep(0.2)
                self.card_uid = None
                self.card_up_callback(uid)

            self._up_task = asyncio.create_task(up_coro())

    def on_card_down(self, callback: Callable):
        self.card_down_callback = callback

    def on_card_up(self, callback: Callable):
        self.card_up_callback = callback
