# Arduino Code

* `chameleon`: arduino for chameleon station
* `crypto`: only functionalities of crypto game
* `dino_run`: dino_run for arduino code, and dino_pc as pc end, receiving singals from arduino. old_python is legacy testing code, not in use.
* `emoji_crypto`: sponsor reader should have functionalities of crypto game according to the settings of HITCON 2023, so it has both emoji and crypto
* `emoji_writer`: only functionalities of emoji game, and can be used as writer, flusher, and eraser
* `initialized_card`: arduino for initialize the card and a python socket server for accumulating the UIDs
* `libs`: general files and reused files, and is used by symlink in other folders
* `popcat`: arduino for popcat game

## Compile

### Files to be changed beforehand

* `libs/master_config.h`

### Commands

```bash
arduino-cli lib install "LiquidCrystal I2C"
arduino-cli lib install MFRC522
arduino-cli lib install ArduinoJson
arduino-cli lib install Crypto

cd popcat
$board=esp8266:esp8266:d1_mini
$file=popcat.ino
sudo chmod a+rw /dev/ttyUSB0

arduino-cli compile --fqbn $board $file
arduino-cli upload -p /dev/ttyUSB0 --fqbn $board $file
arduino-cli monitor -p /dev/ttyUSB0

# or, use one-liner
arduino-cli compile --fqbn $board $file && arduino-cli upload -p /dev/ttyUSB0 --fqbn $board $file && arduino-cli monitor -p /dev/ttyUSB0
```

## TODO

* Improve UX using lcd to display more info. Should integrate the lcd functions in `initialize_card` into libs. (bcuz it's better)
* Use symlink to other modules instead of hardcoding the data and offset in `initialize_card`.
