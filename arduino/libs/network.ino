#include "network.h"
#include <ESP8266HTTPClient.h>


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

	String get_string(const char *path) {
		HTTPClient https;
		int status_code;
		String res;

		https.begin(wifi_client, host, host_port, path);
		status_code = https.GET();
		Serial.printf("status code %d", status_code);
		Serial.println();
		res = https.getString();
		Serial.println("content:");
		Serial.println(res);
		if (status_code == 200)
			return res;
		else
			return "";
	}

	bool get_json(DynamicJsonDocument &doc, const char *path) {
		DeserializationError json_error;

		String data = get_string(path);

		json_error = deserializeJson(doc, data);
		if (json_error) {
			Serial.printf(
				"can't deserialize JSON: %s",
				json_error.f_str()
			);
			Serial.println();
			return false;
		}
		Serial.println("deserialization success");
		return true;
	}

	bool post_json(DynamicJsonDocument &doc, const char *path) {
		String payload;
		HTTPClient https;
		int status_code;
		DeserializationError json_error;

		serializeJson(doc, payload);
		Serial.println("posting:");
		Serial.println(payload);

		https.begin(wifi_client, host, host_port, path);

		status_code = https.POST(payload);
		Serial.printf("status code %d", status_code);
		Serial.println();
		Serial.println("content:");
		Serial.println(https.getString());
		return status_code == 200;
	}
}
