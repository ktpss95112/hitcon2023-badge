import asyncio
from collections.abc import Callable
from datetime import datetime
from typing import Literal

import serial_asyncio


class SerialProtocol(asyncio.Protocol):
    def __init__(self) -> None:
        self.events: dict[str, list[Callable]] = {}
        self.lost_event = asyncio.Event()  # resolve when connection lost

    def connection_made(self, transport):
        self.transport = transport
        print("serial port opened")
        transport.serial.rts = False  # You can manipulate Serial object via transport
        # transport.write(b'Hello, World!\n')  # Write serial data via transport

    def data_received(self, data):
        time_str = datetime.now().astimezone().isoformat()
        print(f"[{time_str}] data received", repr(data))
        for handler in self.events.get("data_received", []):
            handler(data)

    def connection_lost(self, exc):
        print("serial port closed")
        for handler in self.events.get("connection_lost", []):
            handler()
        self.lost_event.set()

    def pause_writing(self):
        print("pause writing")
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        print("resume writing")

    def add_event_listener(self, event: Literal["connection_lost", "data_received"]):
        self.events.setdefault(event, [])

        def inner(handler: Callable):
            self.events[event].append(handler)

        return inner


async def connect_serial(
    serail_port: str, baudrate: int, **kwargs
) -> SerialProtocol | None:
    loop = asyncio.get_event_loop()
    try:
        protocol: SerialProtocol
        transport, protocol = await serial_asyncio.create_serial_connection(
            loop, SerialProtocol, serail_port, baudrate=baudrate, **kwargs
        )
        return protocol
    except:
        return None
