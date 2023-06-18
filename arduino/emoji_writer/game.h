#ifndef _GAME_H
#define _GAME_H

#include <WiFiClientSecureBearSSL.h>
#include "config.h"


namespace game {
	const char *host = GAME_HOST;
	const uint16_t host_port = GAME_HOST_PORT;
	const char *host_fingerprint = GAME_HOST_FINGERPRINT;
	const char *emoji_timetable_path = "/cardreader/emoji_time_table";
	BearSSL::WiFiClientSecure wifi_client;
	void setup();
}

#endif