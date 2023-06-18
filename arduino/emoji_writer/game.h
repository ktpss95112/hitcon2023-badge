#ifndef _GAME_H
#define _GAME_H

#include <WiFiClientSecureBearSSL.h>
#include "config.h"


namespace game {
	const char *host = GAME_HOST;
	const uint16_t host_port = GAME_HOST_PORT;
	const char *host_fingerprint = GAME_HOST_FINGERPRINT;
	const char *client_cert_str = GAME_CLIENT_CERT;
	const char *client_key_str = GAME_CLIENT_KEY;
	const char *emoji_timetable_path = "/cardreader/emoji_time_table";
	BearSSL::WiFiClientSecure wifi_client;
	const BearSSL::X509List client_cert(client_cert_str);
	const BearSSL::PrivateKey client_key(client_key_str);
	void setup();
}

#endif