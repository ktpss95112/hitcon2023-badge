from tkinter import *
from tkinter import ttk
from typing import Callable


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
        self.scan_card_button.grid()
        self.scan_card_button.focus()

        self.show_qrcode_button = ttk.Button(self.frame)
        self.show_qrcode_button["text"] = "Show QR Code"
        self.show_qrcode_button["command"] = show_qrcode_callback
        self.show_qrcode_button.state(["disabled"])
        self.show_qrcode_button.grid()

    def enable_qrcode_button(self):
        self.show_qrcode_button.state(["!disabled"])

    def disable_qrcode_button(self):
        self.show_qrcode_button.state(["disabled"])


class EditorFrame:
    def __init__(self) -> None:
        pass

    def update_content(self):
        pass

    def clear_content(self):
        pass
