import argparse
import asyncio
from pathlib import Path

import aiohttp
from aiohttp import web
from aiohttp.web_urldispatcher import StaticResource

from dino_pc.aio_serial import connect_serial
from dino_pc.cardkey import CardKey


def inject_static():
    _prev_func = StaticResource._directory_as_html

    def _directory_as_html(self, filepath: Path) -> str:
        if Path(filepath, "index.html").is_file():
            return Path(filepath, "index.html").read_text()
        return _prev_func(self, filepath)

    StaticResource._directory_as_html = _directory_as_html


inject_static()

gws: web.WebSocketResponse = None


async def websocket_handler(request):
    global gws

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    print("new websocket connection")
    if gws is None:
        gws = ws
    else:
        await ws.send_json({"error": "window_opened"})
        await ws.close()
        return ws

    async for msg in ws:
        print(msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == "close":
                await ws.close()
            else:
                await ws.send_str(msg.data + "/answer")
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print("ws connection closed with exception %s" % ws.exception())

    print("websocket connection closed")
    gws = None

    return ws


async def main():
    pser = argparse.ArgumentParser()
    pser.add_argument("-p", "--port", type=int, default=8080, help="web listening port")
    pser.add_argument(
        "-s",
        "--serial-port",
        default="/dev/ttyUSB0",
        help="serial port, such as: /dev/ttyUSB0, COM1",
    )
    pser.add_argument("-r", "--baudrate", type=int, default=9600)
    args = pser.parse_args()

    app = web.Application()
    app.add_routes(
        [
            web.get("/ws", websocket_handler),
            web.static("/", Path(__file__, "..", "public"), show_index=True),
        ]
    )

    # non-blocking app runner
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", args.port)
    await site.start()

    web_display_url = "http://localhost"
    if args.port != 80:
        web_display_url = f"{web_display_url}:{args.port}"
    print(f"web server listening on {web_display_url}")
    print("connection to serial...")

    while True:
        serial_proto = await connect_serial(
            serail_port=args.serial_port, baudrate=args.baudrate
        )
        if serial_proto is not None:
            card_key = CardKey(serial_proto)

            @card_key.on_card_down
            def on_card_down(uid: str):
                print(f"card down, uid={uid}")
                if gws is not None:
                    asyncio.create_task(
                        gws.send_json(
                            {
                                "event": "card_down",
                                "uid": uid,
                            }
                        )
                    )

            @card_key.on_card_up
            def on_card_up(uid: str):
                print(f"card up, uid={uid}")
                if gws is not None:
                    asyncio.create_task(
                        gws.send_json(
                            {
                                "event": "card_up",
                                "uid": uid,
                            }
                        )
                    )

            await serial_proto.lost_event.wait()
            print("serial disconnected, try to reconnect")
        await asyncio.sleep(1)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("stop")

import serial

serial.Serial()
