import struct
from collections import UserString
from tkinter import *
from tkinter import font as tkFont
from tkinter import ttk
from typing import Callable, Literal

from .card import card
from .config import config


class UISettingsFrame(ttk.LabelFrame):
    def __init__(self, parent: Misc) -> None:
        self.__fonts = [
            "TkDefaultFont",
            "TkTextFont",
            "TkFixedFont",
            "TkMenuFont",
            "TkHeadingFont",
            "TkCaptionFont",
            "TkSmallCaptionFont",
            "TkIconFont",
            "TkTooltipFont",
        ]
        self.__original_font_size = {
            font_name: tkFont.nametofont(font_name).actual("size")
            for font_name in self.__fonts
        }

        super().__init__(parent)
        self["text"] = "UI Settings"

        label = ttk.Label(self)
        label["text"] = "UI Scale"
        label.grid(column=0, row=0)

        self.__scale_var = StringVar()
        input_box = ttk.Entry(self, textvariable=self.__scale_var)
        input_box.grid(column=1, row=0)

        self.__scale_var.trace_add("write", self.__scale_font)
        self.__scale_var.set(config.DEFAULT_FONT_SCALE)

    def __scale_font(self, *args):
        try:
            scale = float(self.__scale_var.get())
            for font_name in self.__fonts:
                font = tkFont.nametofont(font_name)
                font.configure(size=round(self.__original_font_size[font_name] * scale))
        except:
            pass


class CommandFrame(ttk.LabelFrame):
    def __init__(
        self, parent: Misc, command_scan_card: Callable, command_show_qrcode: Callable
    ) -> None:
        super().__init__(parent)
        self["text"] = "Commands"

        self.__scan_card_button = ttk.Button(self)
        self.__scan_card_button["text"] = "Scan Card"
        self.__scan_card_button["command"] = command_scan_card
        self.__scan_card_button.grid(column=0, row=0)
        self.__scan_card_button.focus()

        self.__show_qrcode_button = ttk.Button(self)
        self.__show_qrcode_button["text"] = "Show QR Code"
        self.__show_qrcode_button["command"] = command_show_qrcode
        self.__show_qrcode_button.grid(column=1, row=0)
        self.disable_qrcode_button()

    def enable_qrcode_button(self):
        self.__show_qrcode_button.state(["!disabled"])

    def disable_qrcode_button(self):
        self.__show_qrcode_button.state(["disabled"])


class EditorFrame(ttk.Frame):
    def __init__(self, parent: Misc, command_scan_card: Callable) -> None:
        super().__init__(parent)

        # setup hex view frame
        self.__hex_view_frame = EditorHexViewFrame(self)
        self.__hex_view_frame.grid(column=0, row=0, sticky=NSEW)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # setup inspect frame
        self.__inspect_frame = EditorInspectFrame(self)
        self.__inspect_frame["padding"] = 5
        self.__inspect_frame.grid(column=1, row=0, sticky=NSEW)

        # setup communication utilities
        self.__hex_view_frame._set_inspect_data_setter(
            self.__inspect_frame._set_inspect_data
        )
        self.__hex_view_frame._set_inspect_write_fields(
            self.__inspect_frame._write_card_fields
        )
        self.__inspect_frame._set_scan_card_command(command_scan_card)

    def update_content(self, data: bytes):
        self.__hex_view_frame._update_content(data)

    def clear_content(self):
        self.__hex_view_frame._update_content(
            b"\x00" * config.NUM_SECTOR * config.NUM_BLOCK * config.BLOCK_SIZE
        )


class EditorHexViewFrame(ttk.Frame):
    """
        Looks like:
    ```
    sector block  0  1  2  3 ... 14 15
       0     0   de ad be ef ... 00 00
             1   40 41 42 43 ... 00 44
             2   40 41 42 43 ... 00 44
             3   40 41 42 43 ... 00 44
       1     0   40 41 42 43 ... 00 44
             1   40 41 42 43 ... 00 44
            ...
      15     0   40 41 42 43 ... 00 44
             1   40 41 42 43 ... 00 44
             2   00 00 00 00 ... 00 00
             3   00 00 00 00 ... 00 00
    ```
    """

    def __init__(self, parent: Misc):
        super().__init__(parent)

        self.__text = Text(self)
        self.__text["wrap"] = "none"
        self.__text.grid(column=0, row=0, sticky=NSEW)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # clear
        self._update_content(
            b"\x00" * config.NUM_SECTOR * config.NUM_BLOCK * config.BLOCK_SIZE
        )

        scrollbar_y = ttk.Scrollbar(self, orient=VERTICAL)
        scrollbar_y["command"] = self.__text.yview
        self.__text["yscrollcommand"] = scrollbar_y.set
        scrollbar_y.grid(column=1, row=0, sticky=NS)

        scrollbar_x = ttk.Scrollbar(self, orient=HORIZONTAL)
        scrollbar_x["command"] = self.__text.xview
        self.__text["xscrollcommand"] = scrollbar_x.set
        scrollbar_x.grid(column=0, row=1, sticky=EW)

        self.__set_callback_on_selection()

    def _set_inspect_write_fields(self, inspect_write_fields: dict[str, StringVar]):
        self.__inspect_write_fields = inspect_write_fields

    def _set_inspect_data_setter(self, inspect_data_setter: Callable):
        self.__inspect_data_setter = inspect_data_setter

    def _update_content(self, data: bytes):
        # ensure that the length of data is correct
        len_ = config.NUM_SECTOR * config.NUM_BLOCK * config.BLOCK_SIZE
        if len(data) < len_:
            data = data.ljust(len_, b"\x00")
        elif len(data) > len_:
            data = data[:len_]

        self.__text.delete("1.0", "end")

        # prepare header
        header_content = ""
        header_content += f"       chunk {0:_^11d}  {1:_^11d}  {2:_^11d}  {3:_^11d}\n"
        header_content += "        byte "
        header_content += "  ".join(
            [
                " ".join(
                    [f"{i:2d}" for i in range(start, start + config.DISPLAY_CHUNK)]
                )
                for start in range(0, config.BLOCK_SIZE, config.DISPLAY_CHUNK)
            ]
        )
        header_content += "\n"
        header_content += "sector block\n"
        self.__text.insert("1.0", header_content)

        # prepare content
        for i_sector in range(config.NUM_SECTOR):
            for i_block in range(config.NUM_BLOCK):
                index = i_sector * config.NUM_BLOCK + i_block
                start = index * config.BLOCK_SIZE
                end = (index + 1) * config.BLOCK_SIZE
                row_data = data[start:end]

                if i_block == 0:
                    self.__text.insert(END, f"{i_sector:^6d} {i_block:^5d} ")
                else:
                    self.__text.insert(END, f"{'':^6} {i_block:^5d} ")

                chunks = [
                    row_data[i_byte : i_byte + config.DISPLAY_CHUNK]
                    for i_byte in range(0, config.BLOCK_SIZE, config.DISPLAY_CHUNK)
                ]
                for i_chunk, chunk in enumerate(chunks):
                    # content
                    chunk_tag = ChunkTag(i_sector, i_block, i_chunk)
                    self.__text.insert(
                        END, " ".join([f"{byte:02x}" for byte in chunk]), (chunk_tag,)
                    )
                    self.__text.insert(
                        END, ("\n" if i_chunk == len(chunks) - 1 else "  ")
                    )
                    self.__text.tag_lower(chunk_tag, belowThis=SEL)

                    # handler
                    def gen_event_handler(
                        chunk_tag: ChunkTag, type_: Literal["enter", "leave", "click"]
                    ):
                        def handler(*args):
                            if chunk_tag.i_block == 3:
                                return
                            if type_ == "click":
                                self.__inspect_write_fields["sector"].set(
                                    chunk_tag.i_sector
                                )
                                self.__inspect_write_fields["block"].set(
                                    chunk_tag.i_block
                                )
                                for i_chunk in range(4):
                                    tag = ChunkTag(
                                        i_sector=chunk_tag.i_sector,
                                        i_block=chunk_tag.i_block,
                                        i_chunk=i_chunk,
                                    )
                                    start, end, *_ = self.__text.tag_ranges(tag)
                                    content = self.__text.get(start, end)
                                    self.__inspect_write_fields[f"data{i_chunk}"].set(
                                        content
                                    )

                                    if i_chunk == chunk_tag.i_chunk:
                                        self.__inspect_data_setter(content)

                            else:
                                bg_color = "" if type_ == "leave" else "yellow"
                                self.__text.tag_configure(
                                    chunk_tag, background=bg_color
                                )

                        return handler

                    # setup handler
                    self.__text.tag_bind(
                        chunk_tag, "<Enter>", gen_event_handler(chunk_tag, "enter")
                    )
                    self.__text.tag_bind(
                        chunk_tag, "<Leave>", gen_event_handler(chunk_tag, "leave")
                    )
                    self.__text.tag_bind(
                        chunk_tag, "<Button-1>", gen_event_handler(chunk_tag, "click")
                    )

        # gray out read-only blocks
        readonly_tag = "readonly"
        self.__text.tag_configure(
            readonly_tag, background="gray90", foreground="gray75"
        )
        self.__text.tag_lower(readonly_tag, belowThis=SEL)
        for i_sector in range(config.NUM_SECTOR):
            for i_chunk in range(config.BLOCK_SIZE // config.DISPLAY_CHUNK):
                chunk_tag = ChunkTag(i_sector, 3, i_chunk)
                start, end, *_ = self.__text.tag_ranges(chunk_tag)
                self.__text.tag_add(readonly_tag, start, end)

    def __set_callback_on_selection(self):
        """
        1. User use cursor to select the text in hex view.
        2. Inspect data is updated automatically.
        """

        def update_inspect_data(*args):
            # If the user do not select anything, just ignore this event.
            if len(self.__text.tag_ranges("sel")) == 0:
                return

            start, end, *_ = self.__text.tag_ranges("sel")
            content = self.__text.get(start, end)
            self.__inspect_data_setter(content)

        self.__text.bind("<<Selection>>", update_inspect_data)


class EditorInspectFrame(ttk.Frame):
    def __init__(self, parent: Misc):
        super().__init__(parent)

        self.__data_view_frame = EditorInspectDataViewFrame(self)
        self.__data_view_frame["padding"] = 5
        self.__data_view_frame.grid(column=0, row=0, sticky=NSEW)

        self.__write_card_frame = EditorInspectWriteCardFrame(self)
        self.__write_card_frame["padding"] = 5
        self.__write_card_frame.grid(column=0, row=1, sticky=NSEW)

        # export some private functions/properties
        self._set_inspect_data = self.__data_view_frame._set_inspect_data
        self._write_card_fields = self.__write_card_frame._write_card_fields
        self._set_scan_card_command = self.__write_card_frame._set_scan_card_command


class EditorInspectDataViewFrame(ttk.LabelFrame):
    def __init__(self, parent: Misc):
        super().__init__(parent)
        self["text"] = "Data Inspector"

        self.__inspect_data = StringVar()
        input_box = ttk.Entry(self, textvariable=self.__inspect_data)
        input_box["font"] = "TkFixedFont"
        input_box.grid(column=0, row=0)

        self.__output_label = ttk.Label(self)
        self.__output_label["font"] = "TkFixedFont"
        self.__output_label.grid(column=0, row=1, sticky=NSEW)

        self.__inspect_data.trace_add("write", self.__update_output)
        self.__inspect_data.set("f0 9f 98 8b")

    def _set_inspect_data(self, content: str):
        self.__inspect_data.set(content)

    def __update_output(self, *args):
        """
        This is the callback function when self.__inspect_data is changed.
        """
        # prepare data
        try:
            data = self.__inspect_data.get().replace(" ", "")
            data_bytes = bytes.fromhex(data).ljust(4, b"\x00")
        except:
            data_bytes = b"\x00" * 4
        try:
            decoded = data_bytes.decode()
        except UnicodeDecodeError:
            decoded = "<error>"

        # prepare output
        self.__output_label[
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


class EditorInspectWriteCardFrame(ttk.LabelFrame):
    def __init__(self, parent: Misc):
        super().__init__(parent)
        self["text"] = "Card Writer"

        def create_field(title, row):
            title_label = ttk.Label(self)
            title_label["text"] = title
            title_label.grid(column=0, row=row, sticky=NSEW)

            strvar = StringVar()
            input_box = ttk.Entry(self, textvariable=strvar)
            input_box["font"] = "TkFixedFont"
            input_box.grid(column=1, row=row)
            self.columnconfigure(1, weight=1)

            return strvar

        self._write_card_fields = {
            "sector": create_field("sector", 0),
            "block": create_field("block", 1),
            **{f"data{i}": create_field(f"data{i}", i + 2) for i in range(4)},
        }

        write_button = ttk.Button(self)
        write_button["text"] = "write card"
        write_button["command"] = self.__write_card
        write_button.grid(column=0, row=len(self._write_card_fields), columnspan=2)

    def _set_scan_card_command(self, scan_card_command: Callable):
        self.__scan_card_command = scan_card_command

    def __write_card(self, *args):
        """
        This is the callback of the "write card" button.
        """
        try:
            sector = int(self._write_card_fields["sector"].get())
            block = int(self._write_card_fields["block"].get())
            data = b"".join(
                [
                    bytes.fromhex(self._write_card_fields[f"data{i}"].get())
                    for i in range(4)
                ]
            )

            card.write_block(data, sector, block)
        except:
            # TODO: error handling (popup error message)
            return

        self.__scan_card_command()


# Just a utility class.
class ChunkTag(UserString):
    def __init__(self, *args, **kwargs) -> None:
        """
        ChunkTag(tag_name)
        ChunkTag(i_sector, i_block, i_chunk)
        """

        if len(args) == 1:
            i_sector, i_block, i_chunk = map(int, args[0].split("."))
        elif len(args) == 3:
            i_sector, i_block, i_chunk = args
        elif len(args) == 0 and len(kwargs) == 3:
            i_sector, i_block, i_chunk = (
                kwargs["i_sector"],
                kwargs["i_block"],
                kwargs["i_chunk"],
            )
        else:
            raise ValueError("Invalid arguments")

        self._i_sector = i_sector
        self._i_block = i_block
        self._i_chunk = i_chunk
        self.data = f"{self._i_sector}.{self._i_block}.{self._i_chunk}"
        super().__init__(f"{i_sector}.{i_block}.{i_chunk}")

    @property
    def i_sector(self):
        return self._i_sector

    @property
    def i_block(self):
        return self._i_block

    @property
    def i_chunk(self):
        return self._i_chunk

    @i_sector.setter
    def i_sector(self, i_sector):
        self._i_sector = i_sector
        self.data = f"{self._i_sector}.{self._i_block}.{self._i_chunk}"

    @i_block.setter
    def i_block(self, i_block):
        self._i_block = i_block
        self.data = f"{self._i_sector}.{self._i_block}.{self._i_chunk}"

    @i_chunk.setter
    def i_chunk(self, i_chunk):
        self._i_chunk = i_chunk
        self.data = f"{self._i_sector}.{self._i_block}.{self._i_chunk}"
