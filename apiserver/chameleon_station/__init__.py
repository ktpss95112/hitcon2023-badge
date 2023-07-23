"""
TODO: features
* scan card and show qrcode for registering DaDi game
* scan card and show hex content (like xxd)
* modify card content arbitrarily
* modify card content (for a specific game)
"""

from tkinter import *
from tkinter import ttk

from . import frames


class ChameleonStation:
    def __init__(self) -> None:
        self.root = root = Tk()
        root.title("Chameleon Station of Badge Mini Games")

        self.command_frame = frames.CommandFrame(
            root,
            scan_card_callback=self.command_scan_card,
            show_qrcode_callback=self.command_show_qrcode,
        )
        self.editor_frame = frames.EditorFrame()

    def command_scan_card(self):
        # TODO: read from arduino
        success = True

        if success:
            self.editor_frame.update_content()
            self.command_frame.enable_qrcode_button()
        else:
            self.editor_frame.clear_content()
            self.command_frame.disable_qrcode_button()

    def command_show_qrcode(self):
        # TODO
        pass

    def mainloop(self):
        return self.root.mainloop()
