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
		fetch_time();
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

		if (data.length() <= 0) {
			Serial.println("empty data");
			return false;
		}

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
		int status_code = -1;
		DeserializationError json_error;

		serializeJson(doc, payload);
		if (payload == "null") {
			/* no null allowed on our server :( */
			payload = "{}";
		}

		if (!https.begin(wifi_client, host, host_port, path)) {
			return false;
		}
		status_code = https.POST(payload);
		payload = https.getString();
		
		json_error = deserializeJson(doc, payload);
		if (json_error) {
			Serial.printf(
				"can't deserialize JSON: %s",
				json_error.f_str()
			);
			return false;
		}
		Serial.println("deserialization success");
		return status_code == 200;
	}

	time_t fetch_time() {
		String datetime_str = get_string(current_time_path);
		if (datetime_str.length() == 0)
			return 0;
		time_t res = util::str_to_epoch(datetime_str.c_str(), "\"%FT%T");
		if (res < DAY2_EPOCH)
			TODAY = 1;
		else
			TODAY = 2;
		Serial.printf("today is %d", TODAY);
		Serial.println();
		return res;
	}
}
