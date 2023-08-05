#include "game.h"
#include "card.h"
#include "util.h"
#include "network.h"
#include <ArduinoJson.h>

namespace game {
    void setup() {
        if (network::fetch_time() <= DAY2_EPOCH)
            TODAY = 1;
        else
            TODAY = 2;
    }

    static bool read_incr(uint32_t *incr) {
        int res = card::pread((byte *)incr, sizeof(incr), incr_off[TODAY]);

        if (res != sizeof(*incr)) {
            Serial.println("Failed to read incr");
            return false;
        }

        return true;
    }

    static int decode_incr_1(uint32_t incr) {
        return (int)incr - 0xaa94237c;
    }

    static int decode_incr_2(uint32_t incr) {
        int16_t upper = incr >> 16;
        int16_t lower = incr & 0xffff;
        return lower - upper;
    }

    int (*decode_incr[])(uint32_t) = {decode_incr_1, decode_incr_2};

    static bool post_incr(int incr, int *cd) {
        byte uid[card::UIDSIZE];
        bool res = card::read_uid(uid);

        *cd = -1;

        if (!res) {
            Serial.println(F("Failed to read the UID"));
            return false;
        }

        String path = incr_path;
        path += "/user/";
        path += util::bytes_to_str(uid, sizeof(uid));
        path += "?incr=";
        path += incr;

        Serial.println("posting to:");
        Serial.println(path);

        DynamicJsonDocument doc(256);

        res = network::post_json(doc, path.c_str());
        if (!res) {
            Serial.println(F("Failed to post the data"));
            return false;
        }

        *cd = doc[1];
        return doc[0];
    }

    void process_card() {
        bool success;
        uint32_t orig_incr;
        int cd, new_incr;
        
        if (!read_incr(&orig_incr))
            return;

        new_incr = decode_incr[TODAY](orig_incr);

        success = post_incr(new_incr, &cd);
        if (success)
            Serial.println("success");
        else
            Serial.println("fail");

        Serial.printf("cooldown: %d", cd);
        Serial.println();
    }
}