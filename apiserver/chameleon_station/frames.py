import struct
from tkinter import *
from tkinter import ttk
from typing import Callable

from .config import config


class CommandFrame:
    def __init__(
        self, parent, scan_card_callback: Callable, show_qrcode_callback: Callable
    ) -> None:
        self.frame = ttk.Frame(parent)
        self.frame["padding"] = 5
        self.frame.grid(column=0, row=0, sticky=(N, E, W))
        parent.columnconfigure(0, weight=1)

        self.scan_card_button = ttk.Button(self.frame)
        self.scan_card_button["text"] = "Scan Card"
        self.scan_card_button["command"] = scan_card_callback
        self.scan_card_button.grid(column=0, row=0)
        self.scan_card_button.focus()

        self.show_qrcode_button = ttk.Button(self.frame)
        self.show_qrcode_button["text"] = "Show QR Code"
        self.show_qrcode_button["command"] = show_qrcode_callback
        self.show_qrcode_button.grid(column=1, row=0)
        self.disable_qrcode_button()

    def enable_qrcode_button(self):
        self.show_qrcode_button.state(["!disabled"])

    def disable_qrcode_button(self):
        self.show_qrcode_button.state(["disabled"])


class EditorFrame:
    def __init__(self, parent) -> None:
        self.frame = ttk.Frame(parent)
        self.frame["padding"] = 5
        self.frame.grid(column=0, row=1, sticky=NSEW)
        parent.columnconfigure(0, weight=1)

        self.setup_hex_view_frame()
        self.setup_editor_frame()

    def setup_hex_view_frame(self):
        self.hex_view_frame = ttk.Frame(self.frame)
        self.hex_view_frame.grid(column=0, row=0, sticky=NSEW)

        self.text = Text(self.hex_view_frame)
        self.text.grid(column=0, row=0, sticky=NSEW)

        self.clear_content()

        scrollbar = ttk.Scrollbar(self.hex_view_frame, orient=VERTICAL)
        scrollbar["command"] = self.text.yview
        self.text["yscrollcommand"] = scrollbar.set
        scrollbar.grid(column=1, row=0, sticky=NS)

    def setup_editor_frame(self):
        self.editor_frame = ttk.Frame(self.frame)
        self.editor_frame["padding"] = 5
        self.editor_frame.grid(column=1, row=0, sticky=NSEW)

        self.inspect_data = StringVar()
        input_box = ttk.Entry(self.editor_frame, textvariable=self.inspect_data)
        input_box["font"] = "TkFixedFont"
        input_box.grid(column=0, row=0)

        output_label = ttk.Label(self.editor_frame, anchor=NW)
        output_label["font"] = "TkFixedFont"
        output_label.grid(column=0, row=1, sticky=NSEW)

        def on_change(*args):
            # prepare data
            try:
                data = self.inspect_data.get().replace(" ", "")
                data_bytes = bytes.fromhex(data).ljust(4, b"\x00")
            except:
                data_bytes = b"\x00" * 4
            try:
                decoded = data_bytes.decode()
            except UnicodeDecodeError:
                decoded = "<error>"

            # prepare output
            output_label[
                "text"
            ] = f"""
uint32: {struct.unpack('<I', data_bytes[0:4])[0]:>19d}
 int32: {struct.unpack('<i', data_bytes[0:4])[0]:>19d}
uint16: {struct.unpack('<H', data_bytes[0:2])[0]:>9d} {struct.unpack('<H', data_bytes[2:4])[0]:>9d}
 int16: {struct.unpack('<h', data_bytes[0:2])[0]:>9d} {struct.unpack('<h', data_bytes[2:4])[0]:>9d}
 uint8: {struct.unpack('<B', data_bytes[0:1])[0]:>4d} {struct.unpack('<B', data_bytes[1:2])[0]:>4d} {struct.unpack('<B', data_bytes[2:3])[0]:>4d} {struct.unpack('<B', data_bytes[3:4])[0]:>4d}
  int8: {struct.unpack('<b', data_bytes[0:1])[0]:>4d} {struct.unpack('<b', data_bytes[1:2])[0]:>4d} {struct.unpack('<b', data_bytes[2:3])[0]:>4d} {struct.unpack('<b', data_bytes[3:4])[0]:>4d}

string: {decoded}
"""

        self.inspect_data.trace_add("write", on_change)
        self.inspect_data.set("f0 9f 98 8b")

    def update_content(self, data: bytes):
        # ensure the size of the data is correct
        len_ = config.NUM_SECTOR * config.NUM_BLOCK * config.BLOCK_SIZE
        if len(data) < len_:
            data = data.ljust(len_, b"\x00")
        elif len(data) > len_:
            data = data[:len_]

        self.data = data
        self._update_content()

    def _update_content(self):
        content = ""
        chunk_size = 4

        # prepare header
        content += f"sector block  "
        content += "  ".join(
            [
                " ".join([f"{i:02x}" for i in range(start, start + chunk_size)])
                for start in range(0, config.BLOCK_SIZE, chunk_size)
            ]
        )
        content += "\n\n"

        # prepare content
        for i_sector in range(config.NUM_SECTOR):
            for i_block in range(config.NUM_BLOCK):
                index = i_sector * config.NUM_BLOCK + i_block
                start = index * config.BLOCK_SIZE
                end = (index + 1) * config.BLOCK_SIZE
                data = self.data[start:end]

                content += f"{i_sector:^6d} {i_block:^5d}  "

                chunks = [
                    data[i_byte : i_byte + chunk_size]
                    for i_byte in range(0, config.BLOCK_SIZE, chunk_size)
                ]
                content += "  ".join(
                    [" ".join([f"{byte:02x}" for byte in chunk]) for chunk in chunks]
                )
                content += "\n"
        content = content.strip("\n")

        self.text.replace("1.0", "end", content)

    def clear_content(self):
        self.data = b"\x00" * config.NUM_SECTOR * config.NUM_BLOCK * config.BLOCK_SIZE
        self._update_content()
