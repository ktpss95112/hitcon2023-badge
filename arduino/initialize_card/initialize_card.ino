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

void setup() {
    Serial.begin(9600);
    lcd.init();
    lcd.backlight();
    card::setup();

    init_network();

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

    // send uid to server
    {
        int count = 0;
        char progress[] = {'|', '-'};
        size_t progress_len = sizeof(progress) / sizeof(char);
        while (!tcp_client.connected()) {
            tcp_client.connect(server_for_uid_upload, port_for_uid_upload);
            delay(500);
            char buf[LCD_LINE_LENGTH * 2 + 1] = {0};
            snprintf(buf, LCD_LINE_LENGTH * 2, "tcp conn lost, retry ... (%c)", progress[count++ % progress_len]);
            lcd_print(buf, 0);
        }
        char buf[2 * card::UIDSIZE + 1] = {0};
        snprintf(buf, 2 * card::UIDSIZE + 1, "%02x%02x%02x%02x", uid[0], uid[1], uid[2], uid[3]);
        tcp_client.print(buf);
        tcp_client.flush();
    }

    card::done();
    {
        char buf[2 * LCD_LINE_LENGTH + 1] = {0};
        snprintf(buf, 2 * LCD_LINE_LENGTH, "Success!        %02x %02x %02x %02x", uid[0], uid[1], uid[2], uid[3]);
        lcd_print(buf, SHORT_SLEEP);
    }
}
