#include "game.h"
#include "card.h"
#include "util.h"
#include "network.h"
#include <ArduinoJson.h>

namespace game {
    void setup() {
        
    }

    static int read_incr_1() {
        int incr;
        int res = card::pread((byte *)&incr, sizeof(incr), raw_incr_off);

        if (res != sizeof(incr)) {
            Serial.println("Failed to read incr");
            return -1;
        }

        return incr;
    }

    static int read_incr_2() {
        int incr;
        int res = card::pread((byte *)&incr, sizeof(incr), xor_incr_off);

        if (res != sizeof(incr)) {
            Serial.println("Failed to read incr");
            return -1;
        }

        return incr ^ 0xdeadbeef;
    }

    static int read_incr() {
        return read_incr_2();
    }

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
        int cd, incr = read_incr();

        if (incr < 0)
            return;

        success = post_incr(incr, &cd);
        if (success)
            Serial.println("success");
        else
            Serial.println("fail");
        Serial.printf("cooldown: %d", cd);
        Serial.println();
    }
}