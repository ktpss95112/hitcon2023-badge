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

## 顧攤須知

![](https://hackmd.io/_uploads/HJyIS1hn2.png)

* 上面的 UI Settings 可以調整視窗字體大小
* 將卡片放在讀卡機上，然後再按 Scan Card，然後等待
    * 做任何操作前都要確保有 Scan Card 過，如果直接點 Show QR Code 的話會是前一次掃的結果！
* block 0 一般而言是不可寫的，只能讀取。隨意改動會導致卡片壞掉！
    * block 0 的 byte 0~3 是 UID，byte 4 是 checksum，必須要等於 byte 0~3 的 byte xor 值。後面的內容是跟製造商有關的
* 畫面上顯示淺灰色底的是每個 sector 的 block 3，這些 block 是用來設定該 sector 功能，並檢查該 sector 是否有被不允許的修改。隨意修改會導致卡片壞掉！
* 滑鼠點選任意的 chunk，在右邊的 Data Inspector 會自動更新成所點選的 chunk。在這邊可以看到這些資料被用不同的格式讀取時分別會長怎樣
* 滑鼠拖曳選取任意長度的內容，被反白的內容會自動被放到 Data Inspector。此功能可用於查看超過 4 byte 長度的字串
* 滑鼠點選任意的 chunk，右邊的 Card Writer 會自動更新成所點選的 chunk。在這邊可以修改卡片的值。請小心不要把卡弄壞！
* 最右邊的 Notes 區可以保存資料，不會受到 Scan Card 或是 write card 等指令而導致資料消失
* 一般而言 UID 是不可寫的，但我們的 badge 是特殊訂製的卡片，是可以複寫 UID 的。用我們的讀卡機讀取自己的證件（如學生證或房卡磁扣），再將該 UID 用 Overwrite UID 的功能來複寫。注意：做此操作前請將自己 badge 原先的 uid 拍照留存，避免喪失遊戲進度。
* 淺藍色底是 emoji 的存放區域，深藍色底是 emoji 的現在長度。右邊的 Emoji Game Inspector 也可以看到當前 emoji 內容。如須清除 emoji，請點選上方 command 的 Clear Emoji Command
* 淺紅色底是 crypto game（數數駭客貓）的存放區域，後面深灰色的區塊是我們的簽章，請不要任意修改！
* 紫色底色是 popcat 的遊戲區塊，兩天會是不同的地區。
