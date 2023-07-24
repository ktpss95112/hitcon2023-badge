"""
TODO: features
* scan card and show qrcode for registering DaDi game
* modify card content arbitrarily
* modify card content (for a specific game)
"""

from tkinter import *
from tkinter import ttk

import PIL.ImageTk
import qrcode

from . import frames
from .card import card
from .config import config


class ChameleonStation:
    def __init__(self) -> None:
        self.root = root = Tk()
        root.title("Chameleon Station of Badge Mini Games")

        self.command_frame = frames.CommandFrame(
            root,
            scan_card_callback=self.command_scan_card,
            show_qrcode_callback=self.command_show_qrcode,
        )
        self.editor_frame = frames.EditorFrame(root)

    def command_scan_card(self):
        # TODO: read from arduino
        # TODO: progress bar
        try:
            data = card.read_all()
            success = True
        except:
            success = False

        if success:
            self.editor_frame.update_content(data)
            self.command_frame.enable_qrcode_button()
        else:
            self.editor_frame.clear_content()
            self.command_frame.disable_qrcode_button()

    def command_show_qrcode(self):
        popup_window = Toplevel(self.root)
        popup_window.geometry(f"{config.QRCODE_SIZE}x{config.QRCODE_SIZE}")

        card_uid = self.data[:4]
        qrcode_content = card_uid.hex()
        self.qrcode_img = PIL.ImageTk.PhotoImage(
            qrcode.make(qrcode_content).resize((config.QRCODE_SIZE, config.QRCODE_SIZE))
        )

        canvas = Canvas(popup_window)
        canvas["width"] = canvas["height"] = config.QRCODE_SIZE
        canvas.grid()
        canvas.create_image(0, 0, image=self.qrcode_img, anchor=NW)

    def mainloop(self):
        return self.root.mainloop()
