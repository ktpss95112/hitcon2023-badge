import struct
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
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
        parent.rowconfigure(1, weight=1)
        parent.columnconfigure(0, weight=1)

        self.setup_hex_view_frame()
        self.setup_editor_frame()

    def setup_hex_view_frame(self):
        """
        Looks like:

        sector block  0  1  2  3 ... 14 15
            0    0   de ad be ef ... 00 00
                 1   40 41 42 43 ... 00 44
                 2   40 41 42 43 ... 00 44
                 3   40 41 42 43 ... 00 44
            1    0   40 41 42 43 ... 00 44
                 1   40 41 42 43 ... 00 44
          ...
           15    0   40 41 42 43 ... 00 44
                 1   40 41 42 43 ... 00 44
                 2   00 00 00 00 ... 00 00
                 3   00 00 00 00 ... 00 00
        """

        self.hex_view_frame = ttk.Frame(self.frame)
        self.hex_view_frame.grid(column=0, row=0, sticky=NSEW)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.hex_view_frame_content = ScrolledText(self.hex_view_frame)
        self.hex_view_frame_content["state"] = "disabled"
        self.hex_view_frame_content["background"] = "white"
        self.hex_view_frame_content.grid(column=0, row=0, sticky=NSEW)
        self.hex_view_frame.rowconfigure(0, weight=1)
        self.hex_view_frame.columnconfigure(0, weight=1)
        # https://stackoverflow.com/a/69936846
        # TODO: bug: cannot scroll when mouse on Frame, but can scroll when on ScrolledText
        inner_frame = ttk.Frame(self.hex_view_frame_content)
        inner_frame.grid()
        self.hex_view_frame_content.window_create("1.0", window=inner_frame)

        self.hex_view_labels = []

        def create_label(text_content, column, row):
            label = ttk.Label(inner_frame)
            label["font"] = "TkFixedFont"
            label["text"] = text_content
            label["background"] = "white"
            label.grid(column=column, row=row)
            return label

        # table header
        # TODO: make bold and color
        headers = ["sector", "block", *(f"{i:2d}" for i in range(config.BLOCK_SIZE))]
        self.hex_view_labels.append(
            [create_label(headers[i], column=i, row=0) for i in range(len(headers))]
        )

        # table content
        for i_sector in range(config.NUM_SECTOR):
            for i_block in range(config.NUM_BLOCK):
                row_index = i_sector * config.NUM_BLOCK + i_block + 1

                sector_label = create_label(
                    i_sector if i_block == 0 else "", column=0, row=row_index
                )
                block_label = create_label(i_block, column=1, row=row_index)
                self.hex_view_labels.append([sector_label, block_label])

                for i_byte in range(config.BLOCK_SIZE):
                    label = create_label("00", column=2 + i_byte, row=row_index)
                    self.hex_view_labels[row_index].append(label)

        self.clear_content()

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

        self._update_content(data)

    def _update_content(self, data: bytes):
        for row_index in range(1, 1 + config.NUM_SECTOR * config.NUM_BLOCK):
            start = (row_index - 1) * config.BLOCK_SIZE
            end = row_index * config.BLOCK_SIZE
            row_data = data[start:end]

            for i_byte in range(config.BLOCK_SIZE):
                self.hex_view_labels[row_index][i_byte + 2][
                    "text"
                ] = f"{row_data[i_byte]:02x}"

    def clear_content(self):
        self._update_content(
            b"\x00" * config.NUM_SECTOR * config.NUM_BLOCK * config.BLOCK_SIZE
        )
