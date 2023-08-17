# Things to change in master_config.h

- the board type (D1R1 or D1R2)
- the WIFI SSID and password
- hostname and port of the API server
- client certificate -- I don't think this should have changed
- (if needed) card reader ID for the emoji game
    - `#define GAME_READER_ID "reader1-1"` for instance
- (if needed) the crypto ID of the card reader
    - `#define DEVCORE` for instance
    - other definition:
        - DEVCORE
        - CYCRAFT
        - FOXCONN
        - ISIP
        - KLICKLACK
        - CHT_SEC
        - TRAPA
        - RAKUTEN
        - KKCOMPANY
        - OFFSEC
        - RESET
        - ADD1
        - ROR
        - SWAP_HILO
        - RAND_FLIP

# compiling and uploading

```bash
cd ./arduino/emoji_crypto # or ./arduino/xxx for other types of card reader
# change $filename to a relevant filename
filename=main.ino; arduino-cli compile --fqbn esp8266:esp8266:d1_mini "$filename" && arduino-cli upload -p /dev/ttyUSB0 --fqbn esp8266:esp8266:d1_mini "$filename"
```