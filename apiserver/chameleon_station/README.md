# Chameleon Station

This is a powerful card manager which should be placed at the information desk of the HITCON activity team. It contains the following functionality:

* Read the RFID card and show the hex dump of the content.
* Show the qrcode which can be used to register the game.
* Modify the card content.

## Prerequisite

[Python interface to Tcl/Tk](https://docs.python.org/3/library/tkinter.html) is a standard Python module. However, you may have to install something like this to continue:

```bash
sudo apt install python3-tk
```

Test with the following command:

```bash
python3 -m tkinter
```

## Run

```bash
python3 -m chameleon_station
```

(hint: remember to `eval $(pdm venv activate)` if needed)
