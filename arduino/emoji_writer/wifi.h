#ifndef _WIFI_H
#define _WIFI_H

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecureBearSSL.h>

namespace wifi {
	static const char *ssid = "aoaaeria";
	static const char *password = "qwfkcwfduqbz";
	static const char *hostname = "aoaauino";

	void setup();
};

#endif
