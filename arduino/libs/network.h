#ifndef _NETWORK_H
#define _NETWORK_H

#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include "config.h"

namespace network {
	const char *ssid = WIFI_SSID;
	const char *password = WIFI_PASSWD;
	const char *hostname = WIFI_HOSTNAME;

	const char *host = GAME_HOST;
	const uint16_t host_port = GAME_HOST_PORT;
	const char *host_fingerprint = GAME_HOST_FINGERPRINT;

	const char *client_cert_str = GAME_CLIENT_CERT;
	const char *client_key_str = GAME_CLIENT_KEY;

	BearSSL::WiFiClientSecure wifi_client;
	const BearSSL::X509List client_cert(client_cert_str);
	const BearSSL::PrivateKey client_key(client_key_str);

	void setup();
	bool get_json(DynamicJsonDocument &doc, const char *path);
	bool post_json(DynamicJsonDocument &doc, const char *path);
};

#endif
