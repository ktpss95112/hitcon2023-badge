# Card Initialization

Should change:
* `card.h`: `RST_PIN` and `SS_PIN` should be consistent with the board.
* `initialization.h`: Change the IP of `server_for_uid_upload`.
* `master_config.h`: `WIFI_SSID` and `WIFI_PASSWD`

Run with:

```bash
sudo chmod a+rw /dev/ttyUSB0
board=esp8266:esp8266:d1_mini
# board=esp8266:esp8266:d1 for d1r1
file=initialize_card.ino
arduino-cli compile --fqbn $board $file && arduino-cli upload -p /dev/ttyUSB0 --fqbn $board $file && arduino-cli monitor -p /dev/ttyUSB0
```
