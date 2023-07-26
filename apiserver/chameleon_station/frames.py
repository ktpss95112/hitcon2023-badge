import struct
from collections import UserString
from tkinter import *
from tkinter import font as tkFont
from tkinter import ttk
from typing import Callable, Literal

from .card import card
from .config import config


class UISettingsFrame:
    def __init__(self, parent) -> None:
        self.fonts = [
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
        self.original_font_size = {
            font_name: tkFont.nametofont(font_name).actual("size")
            for font_name in self.fonts
        }

        self.frame = ttk.LabelFrame(parent)
        self.frame["text"] = "UI Settings"
        self.frame["padding"] = 5
        self.frame.grid(column=0, row=0, sticky=(N, E, W))
        parent.columnconfigure(0, weight=1)

        label = ttk.Label(self.frame)
        label["text"] = "UI Scale"
        label.grid(column=0, row=0)

        self.scale_var = StringVar()
        input_box = ttk.Entry(self.frame, textvariable=self.scale_var)
        input_box.grid(column=1, row=0)

        self.scale_var.trace_add("write", self.scale_font)
        self.scale_var.set(config.DEFAULT_FONT_SCALE)

    def scale_font(self, *args):
        try:
            scale = float(self.scale_var.get())
            for font_name in self.fonts:
                font = tkFont.nametofont(font_name)
                font.configure(size=round(self.original_font_size[font_name] * scale))
        except:
            pass


class CommandFrame:
    def __init__(
        self, parent, command_scan_card: Callable, command_show_qrcode: Callable
    ) -> None:
        self.frame = ttk.LabelFrame(parent)
        self.frame["text"] = "Commands"
        self.frame["padding"] = 5
        self.frame.grid(column=0, row=1, sticky=(N, E, W))
        parent.columnconfigure(0, weight=1)

        self.scan_card_button = ttk.Button(self.frame)
        self.scan_card_button["text"] = "Scan Card"
        self.scan_card_button["command"] = command_scan_card
        self.scan_card_button.grid(column=0, row=0)
        self.scan_card_button.focus()

        self.show_qrcode_button = ttk.Button(self.frame)
        self.show_qrcode_button["text"] = "Show QR Code"
        self.show_qrcode_button["command"] = command_show_qrcode
        self.show_qrcode_button.grid(column=1, row=0)
        self.disable_qrcode_button()

    def enable_qrcode_button(self):
        self.show_qrcode_button.state(["!disabled"])

    def disable_qrcode_button(self):
        self.show_qrcode_button.state(["disabled"])


class EditorFrame:
    def __init__(self, parent, command_scan_card: Callable) -> None:
        self.frame = ttk.Frame(parent)
        self.frame["padding"] = 5
        self.frame.grid(column=0, row=2, sticky=NSEW)
        parent.rowconfigure(2, weight=1)
        parent.columnconfigure(0, weight=1)

        self.setup_hex_view_frame()
        self.setup_inspect_frame(command_scan_card)
        self.set_selection_action()

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

        self.text = Text(self.hex_view_frame)
        self.text["wrap"] = "none"
        self.text.grid(column=0, row=0, sticky=NSEW)
        self.hex_view_frame.rowconfigure(0, weight=1)
        self.hex_view_frame.columnconfigure(0, weight=1)

        self.clear_content()

        scrollbar_y = ttk.Scrollbar(self.hex_view_frame, orient=VERTICAL)
        scrollbar_y["command"] = self.text.yview
        self.text["yscrollcommand"] = scrollbar_y.set
        scrollbar_y.grid(column=1, row=0, sticky=NS)

        scrollbar_x = ttk.Scrollbar(self.hex_view_frame, orient=HORIZONTAL)
        scrollbar_x["command"] = self.text.xview
        self.text["xscrollcommand"] = scrollbar_x.set
        scrollbar_x.grid(column=0, row=1, sticky=EW)

    def setup_inspect_frame(self, command_scan_card: Callable):
        self.inspect_frame = ttk.Frame(self.frame)
        self.inspect_frame["padding"] = 5
        self.inspect_frame.grid(column=1, row=0, sticky=NSEW)

        self.inspect_read_frame = ttk.LabelFrame(self.inspect_frame)
        self.inspect_read_frame["text"] = "Data Inspector"
        self.inspect_read_frame["padding"] = 5
        self.inspect_read_frame.grid(column=0, row=0, sticky=NSEW)

        self.inspect_data = StringVar()
        input_box = ttk.Entry(self.inspect_read_frame, textvariable=self.inspect_data)
        input_box["font"] = "TkFixedFont"
        input_box.grid(column=0, row=0)

        output_label = ttk.Label(self.inspect_read_frame)
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

        self.inspect_write_frame = ttk.LabelFrame(self.inspect_frame)
        self.inspect_write_frame["text"] = "Card Writer"
        self.inspect_write_frame["padding"] = 5
        self.inspect_write_frame.grid(column=0, row=1, sticky=NSEW)

        def create_field(title, row):
            title_label = ttk.Label(self.inspect_write_frame)
            title_label["text"] = title
            title_label.grid(column=0, row=row, sticky=NSEW)

            strvar = StringVar()
            input_box = ttk.Entry(self.inspect_write_frame, textvariable=strvar)
            input_box["font"] = "TkFixedFont"
            input_box.grid(column=1, row=row)
            self.inspect_write_frame.columnconfigure(1, weight=1)

            return strvar

        self.inspect_write_fields = {
            "sector": create_field("sector", 0),
            "block": create_field("block", 1),
            "chunk": create_field("chunk", 2),
            "data": create_field("data", 3),
        }

        def write_card(*args):
            try:
                data = bytes.fromhex(self.inspect_write_fields["data"].get())
                sector = int(self.inspect_write_fields["sector"].get())
                block = int(self.inspect_write_fields["block"].get())
                chunk = int(self.inspect_write_fields["chunk"].get())

                card.write_chunk(data, sector, block, chunk)
            except:
                # TODO: error handling (popup error message)
                return

            command_scan_card()

        write_button = ttk.Button(self.inspect_write_frame)
        write_button["text"] = "write card"
        write_button["command"] = write_card
        write_button.grid(column=0, row=5, columnspan=2)

    def set_selection_action(self):
        """
        1. User use cursor to select the text in hex view.
        2. Inspect data is updated automatically.
        """

        def update_inspect_data(*args):
            # If the user do not select anything, just ignore this event.
            if len(self.text.tag_ranges("sel")) == 0:
                return

            start, end, *_ = self.text.tag_ranges("sel")
            content = self.text.get(start, end)
            self.inspect_data.set(content)

        self.text.bind("<<Selection>>", update_inspect_data)

    def update_content(self, data: bytes):
        # ensure the size of the data is correct
        len_ = config.NUM_SECTOR * config.NUM_BLOCK * config.BLOCK_SIZE
        if len(data) < len_:
            data = data.ljust(len_, b"\x00")
        elif len(data) > len_:
            data = data[:len_]

        self._update_content(data)

    def _update_content(self, data: bytes):
        self.text.delete("1.0", "end")

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
        self.text.insert("1.0", header_content)

        # prepare content
        for i_sector in range(config.NUM_SECTOR):
            for i_block in range(config.NUM_BLOCK):
                index = i_sector * config.NUM_BLOCK + i_block
                start = index * config.BLOCK_SIZE
                end = (index + 1) * config.BLOCK_SIZE
                row_data = data[start:end]

                if i_block == 0:
                    self.text.insert(END, f"{i_sector:^6d} {i_block:^5d} ")
                else:
                    self.text.insert(END, f"{'':^6} {i_block:^5d} ")

                chunks = [
                    row_data[i_byte : i_byte + config.DISPLAY_CHUNK]
                    for i_byte in range(0, config.BLOCK_SIZE, config.DISPLAY_CHUNK)
                ]
                for i_chunk, chunk in enumerate(chunks):
                    # content
                    chunk_tag = ChunkTag(i_sector, i_block, i_chunk)
                    self.text.insert(
                        END, " ".join([f"{byte:02x}" for byte in chunk]), (chunk_tag,)
                    )
                    self.text.insert(
                        END, ("\n" if i_chunk == len(chunks) - 1 else "  ")
                    )
                    self.text.tag_lower(chunk_tag, belowThis=SEL)

                    # handler
                    def gen_event_handler(
                        chunk_tag: ChunkTag, type_: Literal["enter", "leave", "click"]
                    ):
                        def handler(*args):
                            if chunk_tag.i_block == 3:
                                return
                            if type_ == "click":
                                start, end, *_ = self.text.tag_ranges(chunk_tag)
                                content = self.text.get(start, end)
                                self.inspect_data.set(content)
                                self.inspect_write_fields["sector"].set(
                                    chunk_tag.i_sector
                                )
                                self.inspect_write_fields["block"].set(
                                    chunk_tag.i_block
                                )
                                self.inspect_write_fields["chunk"].set(
                                    chunk_tag.i_chunk
                                )
                                self.inspect_write_fields["data"].set(content)
                            else:
                                bg_color = "" if type_ == "leave" else "yellow"
                                self.text.tag_configure(chunk_tag, background=bg_color)

                        return handler

                    # setup handler
                    self.text.tag_bind(
                        chunk_tag, "<Enter>", gen_event_handler(chunk_tag, "enter")
                    )
                    self.text.tag_bind(
                        chunk_tag, "<Leave>", gen_event_handler(chunk_tag, "leave")
                    )
                    self.text.tag_bind(
                        chunk_tag, "<Button-1>", gen_event_handler(chunk_tag, "click")
                    )

        # gray out read-only blocks
        readonly_tag = "readonly"
        self.text.tag_configure(readonly_tag, background="gray90", foreground="gray75")
        self.text.tag_lower(readonly_tag, belowThis=SEL)
        for i_sector in range(config.NUM_SECTOR):
            for i_chunk in range(config.BLOCK_SIZE // config.DISPLAY_CHUNK):
                chunk_tag = ChunkTag(i_sector, 3, i_chunk)
                start, end, *_ = self.text.tag_ranges(chunk_tag)
                self.text.tag_add(readonly_tag, start, end)

    def clear_content(self):
        self._update_content(
            b"\x00" * config.NUM_SECTOR * config.NUM_BLOCK * config.BLOCK_SIZE
        )


# Just a utility class.
class ChunkTag(UserString):
    def __init__(self, *args) -> None:
        """
        ChunkTag(tag_name)
        ChunkTag(i_sector, i_block, i_chunk)
        """

        if len(args) == 1:
            i_sector, i_block, i_chunk = map(int, args[0].split("."))
        elif len(args) == 3:
            i_sector, i_block, i_chunk = args
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
