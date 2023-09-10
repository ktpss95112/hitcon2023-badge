/*
 * BOARD MODEL CONFIGURATION
 * This library is made for Wemos D1 R1 / R2 boards.
 * If you have a different board, please define the IO ports for each libraries.
 */
#define D1R2
// #define D1R1

/*
 * NETWORK CONFIGURATION
 * The SSID / password of the wifi AP, along with the hostname of the board.
 */
#define WIFI_SSID "<redacted>"
#define WIFI_PASSWD "<redacted>"
#define WIFI_HOSTNAME "<redacted>"

/*
 * BOARD-SPECIFIC CONFIGURATION
 * Refer to README.md for more information.
 */
#define DEVCORE
#define GAME_READER_ID "s1"
#define WRITER

// #define CYCRAFT
// #define GAME_READER_ID "s2"
// #define WRITER

// #define FOXCONN
// #define GAME_READER_ID "s3"
// #define WRITER

// #define TRAPA
// #define GAME_READER_ID "s4"
// #define WRITER

// #define CHT_SEC
// #define GAME_READER_ID "s5"
// #define WRITER

// #define RAKUTEN
// #define GAME_READER_ID "s6"
// #define WRITER

// #define OFFSEC
// #define GAME_READER_ID "s7"
// #define WRITER

// #define KKCOMPANY
// #define GAME_READER_ID "s8"
// #define WRITER

// #define ISIP
// #define GAME_READER_ID "s9"
// #define WRITER

// #define KLICKLACK
// #define GAME_READER_ID "s10"
// #define WRITER

// #define GAME_READER_ID "sf1"
// #define FLUSHER

// #define RESET
// #define GAME_READER_ID "c1"

// #define ADD1
// #define GAME_READER_ID "c2"

// #define ROR
// #define GAME_READER_ID "c3"

// #define SWAP_HILO
// #define GAME_READER_ID "c4"

// #define RAND_FLIP
// #define GAME_READER_ID "c5"

// #define GAME_READER_ID "p1"

// #define GAME_READER_ID "p2"

/*
 * Random seed for the crypto game
 */
#define RANDOM_SEED 0xdeadbeef

/*
 * Time between each clock syncs.
 * Shorter interval increases the overhead and the accuracy.
 */
#define CLOCK_SYNC_INTERVAL 100

/*
 * Server and port of the server.
 */
#define GAME_HOST "www.redacted.com"
#define GAME_HOST_PORT 443
/*
 * Certificate fingerprint of the server
 */
#define GAME_HOST_FINGERPRINT "87:87:87:87:87:87:87:87:87:87:87:87:87:87:87:87:87:87:87:87"
/*
 * The game uses SSL client certificate to authenticate the boards.
 */
#define GAME_CLIENT_CERT "-----BEGIN CERTIFICATE-----\n...-----END CERTIFICATE-----\n"
#define GAME_CLIENT_KEY "-----BEGIN PRIVATE KEY-----\n...-----END PRIVATE KEY-----\n"

/*
 * HMAC key for the crypto game in case the participant
 * wants to tamper with the card.
 */
#define GAME_HMAC_KEY {0xe0, 0x72, 0x77, 0x6f, 0x57, 0x99, 0x6c, 0x89}
