# hitcon2023-badge (HITCON CMT 2023)

* Official document: [link](https://docs.google.com/document/d/1-b-IGACYCKCki-YTx9WcoPfhuFjb6nA6ySIB4u-Rhjk/edit?usp=sharing)
* Team members:
    * @ktpss95112 (leader)
    * @Alx-Lai
    * @aoaaceai
    * @doraeric
    * @Simteng
    * special thanks to @john0312

## Chameleon Station

This is the super card reader/writer placed at the information desk of the HITCON activity team. Please refer to the folder `chameleon_station`.

## API Server

This is the server which process all the game event. It would be accessed by all the arduino through WiFi. It may also be accessed by other activity (such as dashboard and 大地遊戲).

## Game Specification

(copied from dev hackmd)

### 遊戲一：啵啵！駭客貓
（內部 code name: popcat）

* 遊戲機制
    * 每隔 120 秒可以刷一次
        * TODO: 間隔的秒數可以隨時間變化，例如第一天 5min，第二天 2min
    * 卡片上有一個 uint32_t 存一個 `encode(incr)`，incr 初始化成 1，代表每次刷卡會加 1
        * encode 的演算法現在設計成 `lambda x: x + 1337`，decode 是做在 arduino 上的，api server 會直接記錄收到的 `incr`
        * 會眾可以改這個 block 來影響 decode 過後的東西，這是 intended 的，但他們需要先猜出我們怎麼 encode/decode 的
        * 第一天：encode 定義為 `lambda x: x + 0xaa94237c`，decode 定義為 `lambda x: x - 0xaa94237c`。得到的數值 cast 成 int32_t（值域 $[-2147483648, 2147483647)$）
        * 第二天：encode 和 decode 定義為
          ```c
          uint32_t encode(int16_t x) {
              int16_t r = rand();
              return (r << 16) + (int16_t(r + x))
          }
          int16_t decode(uint32_t x) {
              int16_t upper = (x >> 16);
              int16_t lower = (x & 0xffff);
              return lower - upper;
          }
          ```
    * 排行榜的分數計分至 16:00
* 獎品
    * 共 20 份
    * 每日分數排名最高的 8 位和最低的 2 位，共 2 日（同分則增額給予獎品）


### 遊戲二：跑跑！駭客貓
（內部 code name: dinorun）

* 遊戲機制
    * chrome 離線恐龍，貼皮成駭客貓
    * 玩家靠卡感應，當作一般遊玩情況的鍵盤 input
    * 遊戲結束後遊戲主程式將玩家分數上傳到 api server
* 獎品
    * 共 20 份
    * 每日分數排名最高的 10 位，共 2 日（同分則增額給予獎品）


### 遊戲三：數數！駭客貓
（內部 code name: crypto game）

* 遊戲機制
    * 每張卡片會有一個 uint32_t 的空間存一個數字 $x$；會場中各處有讀卡機，每台讀卡機各自代表一個對 $x$ 做的操作 (inplace)，這個操作的內容是公開的，會貼在讀卡機上
    * 每日公佈一個 target 數字 $y$，玩家需要以特定順序刷過不同的讀卡機，使得 $x$ 最終變成 $y$
    * 卡片上有另一個空間存 `concat(x, card_uid)` 的 hmac，所有讀卡機共享一個 hmac 的 key
        * ```python
          import hmac

          key = b'\xde\xad\xbe\xef'
          card_uid = b'\xde\xad\xbe\xef'
          data = b'aaaa'

          h = hmac.new(key, digestmod='sha256')
          h.update(card_uid)
          h.update(data)
          print(h.hexdigest())
          ```
    * 活動組攤位檢查玩家的 hmac 是否是由 `concat(x, card_uid)` 得來的，滿足的話即可獲得獎品（每日限額）
    * 第一天：
        * $y = 462336$
            * 官方解法：0
              -> (wild2 7 次) -> 7
              -> (wild3 1 次) -> 234881024
              -> (wild2 3 次) -> 234881027
              -> (wild4 1 次) -> 462336
        * 各機臺功能如下
          ```c
          #ifdef DEVCORE
          static uint32_t update_data(uint32_t src) {
              static char str[] = "DVCR";
              return src ^ *(int *)str;
          }
          #elif defined CYCRAFT
          static uint32_t update_data(uint32_t src) {
                static char str[] = "CRFT";
                return src ^ *(int *)str;
          }
          #elif defined FOXCONN
          static uint32_t update_data(uint32_t src) {
              static char str[] = "2317";
              return src ^ *(int *)str;
          }
          #elif defined ISIP
          static uint32_t update_data(uint32_t src) {
              static char str[] = "ISIP";
              return src ^ *(int *)str;
          }
          #elif defined KLICKLACK
          static uint32_t update_data(uint32_t src) {
              static char str[] = "KKCO";
              return src ^ *(int *)str;
          }
          #elif defined CHT_SEC
          static uint32_t update_data(uint32_t src) {
              static char str[] = "CHTS";
              return src ^ *(int *)str;
          }
          #elif defined TRAPA
          static uint32_t update_data(uint32_t src) {
              static char str[] = "TRPA";
              return src ^ *(int *)str;
          }
          #elif defined RAKUTEN
          static uint32_t update_data(uint32_t src) {
              static char str[] = "RKTN";
              return src ^ *(int *)str;
          }
          #elif defined KKCOMPANY
          static uint32_t update_data(uint32_t src) {
              static char str[] = "KBOX";
              return src ^ *(int *)str;
          }
          #elif defined OFFSEC
          static uint32_t update_data(uint32_t src) {
              static char str[] = "OFSC";
              return src ^ *(int *)str;
          }
          uint32_t wild1(uint32_t x) { // just reset
              // IMPORTANT: do not check hmac!
              return 0;
          }
          uint32_t wild2(uint32_t x) {
              return x + 1;
          }
          uint32_t wild3(uint32_t x) {
              // uint5_t r = LSB 5 bit
              // ror(x, r)
              return ;
          }
          uint32_t wild4(uint32_t x) {
              // low 16 bits swap with high 16 bits
              return ;
          }
          uint32_t wild5(uint32_t x) {
              // random flip 2 bits
              return ;
          }
          ```
    * 第二天：
        * $y = 1056$
            * 官方解法
            * 0
              -> (sponsor02 1 次) -> 1413894723
              -> (wild4 1 次) -> 1380144198
              -> (+5) -> 1380144203
              -> (sponsor01 1 次) -> 527
              -> (wild3 1 次) -> 69074944
              -> (wild4 1 次) -> 1054
              -> (+2) -> 1056
            * 0
              -> (wild5) -> 1056
            * validate: https://gist.github.com/Alx-Lai/6cca55436cae327f76d23d7bb9400b30
* 獎品
    * 共 20 份
    * 每日的前 10 名可獲獎，第一天如獎品有剩則第二天仍可提交第一天之解答並領獎
