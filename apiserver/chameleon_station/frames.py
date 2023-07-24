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

        self.text = Text(self.frame)
        self.text.grid(column=0, row=0, sticky=NSEW)

        self.update_content(
            b"\x00" * config.NUM_SECTOR * config.NUM_BLOCK * config.BLOCK_SIZE
        )

        self.scrollbar = ttk.Scrollbar(self.frame, orient=VERTICAL)
        self.scrollbar["command"] = self.text.yview
        self.text["yscrollcommand"] = self.scrollbar.set
        self.scrollbar.grid(column=1, row=0, sticky=NS)

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
        pass
