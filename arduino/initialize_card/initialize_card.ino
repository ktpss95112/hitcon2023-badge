#include <stdint.h>
#include "card.h"

#include <SHA256.h>

#define GAME_HMAC_KEY {0xde, 0xad, 0xbe, 0xef, 0xca, 0xfe, 0xba, 0xbe}


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
    card::setup();
}

void loop() {
    if (!card::legal_new_card())
        return;

    byte uid[card::UIDSIZE];
    int res = card::read_uid(uid);
    if (!res) {
        Serial.println("failed to read the UID");
        return;
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
            Serial.println("emoji pwrite failed");
            return;
        }
        Serial.println("emoji initialized");
    }

    // popcat
    {
        uint32_t day1 = 0xaa94237cU + 1;
        uint32_t r = random(0, (1u << 16));
        uint32_t day2 = (r << 16) + uint16_t(r + 1);
        if (card::pwrite((byte *)&day1, sizeof(int), popcat_day1_off) != sizeof(int)) {
            Serial.println("popcat pwrite day1 failed");
            return;
        }
        if (card::pwrite((byte *)&day2, sizeof(int), popcat_day2_off) != sizeof(int)) {
            Serial.println("popcat pwrite day2 failed");
            return;
        }
        Serial.println("popcat initialized");
    }

    // crypto
    {
		byte hmac[hmac256::HMACSIZE];
        uint32_t data = 0;
		hmac256::gen_hmac((byte *)&data, sizeof(data), uid, hmac);
		if (card::pwrite((byte *)&data, sizeof(data), crypto_data_off) != sizeof(data)) {
            Serial.print("crypto pwrite data failed");
            return;
        }
		if (card::pwrite(hmac, sizeof(hmac), crypto_hmac_off) != sizeof(hmac)) {
            Serial.print("crypto pwrite hmac failed");
            return;
        }
        Serial.println("crypto initialized");
    }


    card::done();
}
