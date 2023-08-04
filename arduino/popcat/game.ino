#include "game.h"
#include "card.h"
#include "util.h"
#include "network.h"
#include <ArduinoJson.h>

namespace game {
    void setup() {
        
    }

    static int read_count() {
        int cnt;
        int res = card::pread((byte *)&cnt, sizeof(cnt), incr_off);

        if (res != sizeof(cnt)) {
            Serial.println("Failed to read incr");
            return 0;
        }

        return cnt;
    }

    static bool post_count(int cnt) {
        byte uid[16];
        bool res = card::read_uid(uid);
        if (!res) {
            Serial.println(F("Failed to read the UID"));
            return false;
        }

        String path = incr_path;
        path += "/user/";
        path += util::bytes_to_str(uid, sizeof(uid));

        DynamicJsonDocument doc(64);
        doc["incr"] = cnt;

        return network::post_json(doc, path.c_str());
    }

    void process_card() {
        int cnt = read_count();
        post_count(cnt);
    }
}