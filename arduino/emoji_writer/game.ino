#include <time.h>
#include <ArduinoJson.h>
#include <ESP8266HTTPClient.h>
#include "game.h"

namespace game {
	static bool get_json(DynamicJsonDocument &doc, const char *path) {
		HTTPClient https;
		int status_code;
		DeserializationError json_error;

		if (!https.begin(wifi_client, host, host_port, path)) {
			Serial.printf("failed connecting to %s%s", host, path);
			Serial.println();
			return false;
		}

		status_code = https.GET();
		if (status_code != 200) {
			Serial.printf("status code %d", status_code);
			Serial.println();
			return false;
		}

		json_error = deserializeJson(doc, https.getStream());
		if (json_error) {
			Serial.printf(
				"can't deserialize JSON: %s",
				json_error.f_str()
			);
			Serial.println();
			return false;
		}
		return true;
	}

	static void store_one_emoji(const JsonVariant &doc) {
		const char *datetime_str = doc[1];
		tm datetime {0};
		strptime(datetime_str, "%FT%T.", &datetime);
		/* TODO: store it somewhere in the memory */
	}

	static bool read_timetable() {
		int i, n;
		DynamicJsonDocument doc(256);
		if (!get_json(doc, emoji_timetable_path))
			return false;

		n = doc.size();
		for (i = 0; i < n; ++i)
			store_one_emoji(doc[i]);
		return true;
	}

	void setup() {
		wifi_client.setClientRSACert(&client_cert, &client_key);
		wifi_client.setFingerprint(host_fingerprint);
		read_timetable();
	}
}
