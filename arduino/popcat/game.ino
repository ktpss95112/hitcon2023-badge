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
        byte uuid[16];
        bool res = card::read_uuid(uuid);
        if (!res) {
            Serial.println(F("Failed to read the UUID"));
            return false;
        }

        String path = incr_path;
        path += "/user/";
        path += util::bytes_to_str(uuid, sizeof(uuid));

        DynamicJsonDocument doc(64);
        doc["incr"] = cnt;

        return network::post_json(doc, path.c_str());
    }

    void process_card() {
        int cnt = read_count();
        post_count(cnt);
    }
}