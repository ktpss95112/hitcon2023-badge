#ifndef _WIFI_H
#define _WIFI_H

#include <ESP8266WiFi.h>
#include "config.h"

namespace wifi {
	const char *ssid = WIFI_SSID;
	const char *password = WIFI_PASSWD;
	const char *hostname = WIFI_HOSTNAME;

	void setup();
};

#endif
