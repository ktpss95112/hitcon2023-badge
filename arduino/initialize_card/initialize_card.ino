#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "master_config.h"
#include "card.h"
#include "initialize_card.h"

#include <SHA256.h>
#include <LiquidCrystal_I2C.h>


#include <SPI.h>
#include <MFRC522.h>


const size_t LCD_LINE_LENGTH = 16;
LiquidCrystal_I2C lcd(0x27, 16, 2);
const int ERR_SLEEP = 2000;
const int NORMAL_SLEEP = 1000;
const int SHORT_SLEEP = 500;

namespace hmac256 {
    static bool arr_eq(const byte *a, const byte *b, int len) {
        for (int i = 0; i < len; ++i) {
            if (a[i] != b[i])
                return false;
        }

        return true;
    }

    const int HMACSIZE = 32;
    const byte hmac_key[] = GAME_HMAC_KEY;
    void gen_hmac(byte *data, int len, byte *uid, byte *dest) {
        SHA256 hash;
        hash.resetHMAC(hmac_key, sizeof(hmac_key));
        hash.update(uid, card::UIDSIZE);
        hash.update(data, len);
        hash.finalizeHMAC(hmac_key, sizeof(hmac_key), dest, HMACSIZE);
    }
}

void lcd_print(const char *str, int sleep) {
    Serial.println(str);  // for debugging

    static char cache[LCD_LINE_LENGTH * 2 + 1] = {0};
    if (strncmp(cache, str, 2 * LCD_LINE_LENGTH) == 0) {
        delay(sleep);
        return;
    }

    size_t len = strnlen(str, 2 * LCD_LINE_LENGTH);

    lcd.clear();
    if (len <= LCD_LINE_LENGTH) {
        lcd.setCursor(0, 0);
        lcd.print(str);
    } else {
        char str2[LCD_LINE_LENGTH + 1] = {0};
        strncpy(str2, str, LCD_LINE_LENGTH);
        lcd.setCursor(0, 0);
        lcd.print(str2);
        strncpy(str2, str + LCD_LINE_LENGTH, LCD_LINE_LENGTH);
        lcd.setCursor(0, 1);
        lcd.print(str2);
    }
    strncpy(cache, str, 2 * LCD_LINE_LENGTH);

    delay(sleep);  // rate limit
}

void setup() {
    Serial.begin(9600);
    lcd.init();
    lcd.backlight();
    card::setup();

    lcd_print("Initialized.", NORMAL_SLEEP);
}

void loop() {
    lcd_print("Waiting for new card ...", 0);

    if (!card::legal_new_card())
        return;

    byte uid[card::UIDSIZE];
    int res = card::read_uid(uid);
    if (!res) {
        lcd_print("failed to read the UID", ERR_SLEEP);
        return;
    } else {
        char buf[2 * LCD_LINE_LENGTH + 1] = {0};
        snprintf(buf, 2 * LCD_LINE_LENGTH, "Card detected.  %02x %02x %02x %02x", uid[0], uid[1], uid[2], uid[3]);
        lcd_print(buf, SHORT_SLEEP);
    }

    // TODO: include header file from other folder instead of hard-coding
    const int emoji_start_off = 0;
    const int emoji_size = card::BLKSIZE * 14 - sizeof(unsigned);
    const int emoji_len_off = emoji_size;
    const int popcat_day1_off = 20 * card::BLKSIZE;
    const int popcat_day2_off = popcat_day1_off + sizeof(int);
    const int crypto_data_off = 272;
    const int crypto_hmac_off = crypto_data_off + card::BLKSIZE;

    // emoji
    {
        int zero = 0;
        if (card::pwrite((byte *)&zero, sizeof(int), emoji_len_off) != sizeof(int)) {
            lcd_print("emoji pwrite failed", ERR_SLEEP);
            return;
        }
        // lcd_print("emoji initialized");
    }

    // popcat
    {
        uint32_t day1 = 0xaa94237cU + 1;
        uint32_t r = random(0, (1u << 16));
        uint32_t day2 = (r << 16) + uint16_t(r + 1);
        if (card::pwrite((byte *)&day1, sizeof(int), popcat_day1_off) != sizeof(int)) {
            lcd_print("popcat pwrite day1 failed", ERR_SLEEP);
            return;
        }
        if (card::pwrite((byte *)&day2, sizeof(int), popcat_day2_off) != sizeof(int)) {
            lcd_print("popcat pwrite day2 failed", ERR_SLEEP);
            return;
        }
        // lcd_print("popcat initialized");
    }

    // crypto
    {
        byte hmac[hmac256::HMACSIZE];
        uint32_t data = 0;
        hmac256::gen_hmac((byte *)&data, sizeof(data), uid, hmac);
        if (card::pwrite((byte *)&data, sizeof(data), crypto_data_off) != sizeof(data)) {
            lcd_print("crypto pwrite data failed", ERR_SLEEP);
            return;
        }
        if (card::pwrite(hmac, sizeof(hmac), crypto_hmac_off) != sizeof(hmac)) {
            lcd_print("crypto pwrite hmac failed", ERR_SLEEP);
            return;
        }
        // lcd_println("crypto initialized");
    }

    card::done();
    {
        char buf[2 * LCD_LINE_LENGTH + 1] = {0};
        snprintf(buf, 2 * LCD_LINE_LENGTH, "Success!        %02x %02x %02x %02x", uid[0], uid[1], uid[2], uid[3]);
        lcd_print(buf, SHORT_SLEEP);
    }
}
