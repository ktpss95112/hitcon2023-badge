import serial as pyserial
from time import sleep, time
import atexit
import asyncio

# config
port = '/dev/ttyUSB0'
width = 0x40
height = 5
game_cycle = 1 # second(s)

def print_menu(lines : str):
    # print string and will be clean at next print
    # avoid buffering
    lines = lines.split('\n')
    line_count = len(lines)
    for i in range(len(lines)):
        lines[i] = lines[i].ljust(width)
    lines = '\n'.join(lines)
    # to fix not support multiline clean
    print(lines, end='\r' * line_count, flush=True)

async def get_tap():
    return serial.read_all().strip()

def game_start():
    print_menu("tab\nto\nstart")

def update_pos(pos):
    if pos == height:
        pos = -height+1
    elif pos != 0:
        pos += 1
    return pos

def draw(pos):
    s = (abs(pos) * '_' + 'X').ljust(width)
    print_menu(s)

async def game():
    pos = 0
    while True:
        # timeout tap
        start_time = time()
        tap = await asyncio.wait_for(get_tap(), timeout=game_cycle)
        # game
        pos = update_pos(pos)
        if tap and pos == 0:
            pos += 1
        draw(pos)
        end_time = time()
        await asyncio.sleep(game_cycle - (end_time - start_time))

def main():
    game_start()
    asyncio.run(game())

serial = pyserial.Serial(port)
atexit.register(serial.close)
main()
