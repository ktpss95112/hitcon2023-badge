# Chameleon Station

This is a powerful card manager which should be placed at the information desk of the HITCON activity team. It contains the following functionality:

* Read the RFID card and show the hex dump of the content.
* Show the qrcode which can be used to register the game.
* Modify the card content.

## Prerequisite

### UI

[Python interface to Tcl/Tk](https://docs.python.org/3/library/tkinter.html) is a standard Python module. However, you may have to install something like this to continue:

```bash
sudo apt install python3-tk
```

Test with the following command:

```bash
python3 -m tkinter
```

TODO: Use web (html/css/js) instead of tkinter. The UI of tkinter has bad support on emoji rendering (so painful).

### Arduino

This module use `pyserial` to interact with arduino. Please make sure that the arduino is uploaded with the correct module.

On Ubuntu (or similar Linux platforms), if you encounter permission error on `/dev/ttyUSB0`, please use `sudo chmod a+rw /dev/ttyUSB0` to give iit permission. If you see something like `/dev/ttyUSB1` or other names, please unplug the USB and re-plug it, or modify the `SERIAL_PORT` in `config.py`.

If you don't have an arduino plugged into your computer, the program can still be started. Only that the content of the card is randomly generated instead of read from a real card.

## Run

```bash
pdm run python -m chameleon_station
```
