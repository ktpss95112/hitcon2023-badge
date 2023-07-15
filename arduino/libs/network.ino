#include "network.h"

namespace network {
	void setup() {
		WiFi.hostname(hostname);
		WiFi.begin(ssid, password);
		Serial.println(F("Connecting to wifi..."));
		while (WiFi.status() != WL_CONNECTED) {
			delay(500);
			Serial.print(F("."));
		}
		Serial.println(F(""));
		Serial.print(F("IP: "));
		Serial.println(WiFi.localIP());

		wifi_client.setClientRSACert(&client_cert, &client_key);
		wifi_client.setFingerprint(host_fingerprint);
	}

	bool get_json(DynamicJsonDocument &doc, const char *path) {
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

	bool post_json(DynamicJsonDocument &doc, const char *path) {
		String payload;
		HTTPClient https;
		int status_code;
		DeserializationError json_error;

		serializeJson(doc, payload);

		if (!https.begin(wifi_client, host, host_port, path)) {
			Serial.printf("failed connecting to %s%S", host, host_port);
			Serial.println();
			return false;
		}

		status_code = https.POST(payload);
		if (status_code != 200) {
			Serial.printf("status code %d", status_code);
			Serial.println();
			return false;
		}
		return true;
	}
}
