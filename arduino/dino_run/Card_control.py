import asyncio
import atexit
from time import time

import serial as pyserial

import Const
from EventManager import *

# TODO: merge into controller.py

# config
# TODO: to dataclass
port = "/dev/ttyUSB0"
game_cycle = 1 / Const.FPS / 2
timeout = game_cycle / 2  # second(s)

serial = pyserial.Serial(port)
atexit.register(serial.close)


async def get_tap():
    return len(serial.read_all().strip()) > 0


async def game_control(ev_manager):
    start_time = time()
    tap = await asyncio.wait_for(get_tap(), timeout=timeout)
    # game
    if tap:
        ev_manager.post(EventPlayerJump())
    end_time = time()
    await asyncio.sleep(game_cycle - (end_time - start_time))
