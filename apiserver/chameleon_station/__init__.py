"""
TODO: features
* scan card (arduino)
* modify card content arbitrarily (arduino)
* modify card content (for a specific game)
"""

from tkinter import *
from tkinter import ttk

from . import frames


class ChameleonStation:
    def __init__(self) -> None:
        self.root = root = Tk()
        root.title("Chameleon Station of Badge Mini Games")
        root.geometry("1400x900")

        self.ui_settings_frame = frames.UISettingsFrame(root)
        self.ui_settings_frame["padding"] = 5
        self.ui_settings_frame.grid(column=0, row=0, sticky=(N, E, W))
        self.root.columnconfigure(0, weight=1)

        self.command_frame = frames.CommandFrame(root)
        self.command_frame["padding"] = 5
        self.command_frame.grid(column=0, row=1, sticky=(N, E, W))
        self.root.columnconfigure(0, weight=1)

        self.editor_frame = frames.EditorFrame(root, command_frame=self.command_frame)
        self.editor_frame["padding"] = 5
        self.editor_frame.grid(column=0, row=2, sticky=NSEW)
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)

    def mainloop(self):
        return self.root.mainloop()
