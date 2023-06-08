#ifndef _WIFI_H
#define _WIFI_H

#include <ESP8266WiFi.h>
#include "config.h"

namespace wifi {
	static const char *ssid = WIFI_SSID;
	static const char *password = WIFI_PASSWD;
	static const char *hostname = WIFI_HOSTNAME;

	void setup();
};

#endif
