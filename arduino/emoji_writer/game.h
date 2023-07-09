#ifndef _GAME_H
#define _GAME_H

#include <WiFiClientSecureBearSSL.h>
#include "config.h"
#include "card.h"


namespace game {
	struct emoji_timetable {
		time_t starttime;
		String emoji;
		std::shared_ptr<emoji_timetable> next;
		emoji_timetable(
			time_t starttime, const char *emoji,
			std::shared_ptr<emoji_timetable> next
		) : starttime(starttime), emoji(emoji), next(next) {}
	};
	const char *host = GAME_HOST;
	const uint16_t host_port = GAME_HOST_PORT;
	const char *host_fingerprint = GAME_HOST_FINGERPRINT;

	const char *client_cert_str = GAME_CLIENT_CERT;
	const char *client_key_str = GAME_CLIENT_KEY;

	const char *reader_id = GAME_READER_ID;

	const char *emoji_timetable_path = "/cardreader/emoji_time_table/" GAME_READER_ID;
	const char *current_time_path = "/time";
	const char *flush_path = "/tap/sponsor_flush_emoji/";

	const unsigned capacity = card::BLKSIZE * 13 - sizeof(unsigned);
	const unsigned strlen_off = capacity;

	BearSSL::WiFiClientSecure wifi_client;
	const BearSSL::X509List client_cert(client_cert_str);
	const BearSSL::PrivateKey client_key(client_key_str);
	time_t clock_offset = 0;
	clock_t clock_last_update = 0;
	std::shared_ptr<emoji_timetable> emoji_timetable_head = NULL;

	void setup();
	void writer_loop();
	void eraser_loop();
	void flusher_loop();
}

#endif