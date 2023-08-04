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

    static bool read_incr(int *incr) {
        int res = card::pread((byte *)incr, sizeof(incr), incr_off[TODAY]);

        if (res != sizeof(*incr)) {
            Serial.println("Failed to read incr");
            return false;
        }

        return true;
    }

    // TODO: change the name (and implementation) of these two functions
    static int decode_incr_1(int incr) {
        return incr;
    }

    static int decode_incr_2(int incr) {
        return incr ^ 0xdeadbeef;
    }

    int (*decode_incr[])(int) = {decode_incr_1, decode_incr_2};

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
        int cd, incr;
        
        if (!read_incr(&incr))
            return;

        incr = decode_incr[TODAY](incr);

        success = post_incr(incr, &cd);
        if (success)
            Serial.println("success");
        else
            Serial.println("fail");

        Serial.printf("cooldown: %d", cd);
        Serial.println();
    }
}