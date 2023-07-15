#include "wifi.h"

namespace wifi {
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
	}
}
