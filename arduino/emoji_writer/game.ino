#include <time.h>
#include <ArduinoJson.h>
#include <ESP8266HTTPClient.h>
#include <memory>
#include "game.h"
#include "card.h"
#include "network.h"

namespace game {
	static time_t str_to_epoch(const char *str) {
		tm datetime {0};
		strptime(str, "%FT%T.", &datetime);
		return mktime(&datetime);
	}

	static void push_one_emoji(const JsonVariant &doc) {
		const char *starttime_str = doc[0];
		const char *emoji_str = doc[1];
		time_t starttime = str_to_epoch(starttime_str);
		std::shared_ptr<emoji_timetable> cur(new emoji_timetable(
			starttime, emoji_str, emoji_timetable_head
		));
		emoji_timetable_head = cur;
	}

	static void pop_one_emoji() {
		emoji_timetable_head = emoji_timetable_head->next;
	}

	static bool read_timetable() {
		int i, n;
		DynamicJsonDocument doc(256);
		if (!network::get_json(doc, emoji_timetable_path))
			return false;

		n = doc.size();
		/*
		 * Since the timetable in the server is in ascending order,
		 * we reverse it here so the head is the earliest entry.
		 */
		for (i = n-1; i >= 0; --i)
			push_one_emoji(doc[i]);
		return true;
	}

	static time_t seconds_from_boot() {
		return millis() / 1000;
	}

	static time_t estimated_cur_time() {
		return clock_offset + seconds_from_boot();
	}

	static bool sync_clock() {
		DynamicJsonDocument doc(48);
		if (!network::get_json(doc, current_time_path))
			return false;
		String datetime_str = doc.as<String>();
		time_t now = str_to_epoch(datetime_str.c_str());
		clock_offset = now - seconds_from_boot();
		clock_last_update = seconds_from_boot();
		return true;
	}

	static int get_cur_len() {
		unsigned cur_len;
		int res = card::pread((byte *)&cur_len, sizeof(cur_len), strlen_off);
		if (res != sizeof(cur_len))
			return -1;
		return min(capacity, cur_len);
	}

	void setup() {
		if (!sync_clock()) {
			Serial.println("clock synchronization failed");
			return;
		}
		if (!read_timetable()) {
			Serial.println("time table read failed");
			return;
		}
	}

	static void clock_housekeeping() {
		if (seconds_from_boot() < clock_last_update + CLOCK_SYNC_INTERVAL)
			return;
		sync_clock();
	}

	static void timetable_housekeeping() {
		while (
			emoji_timetable_head->next &&
			emoji_timetable_head->next->starttime <= estimated_cur_time()
		)
			pop_one_emoji();
	}

	static void write_card() {
		int cur_len = get_cur_len();
		if (cur_len < 0) {
			Serial.println("failed to read the current length");
			return;
		}
		String &cur_emoji = emoji_timetable_head->emoji;
		int emoji_len = cur_emoji.length();
		if (cur_len + emoji_len >= capacity) {
			/* TODO: perhaps beep in a different tone */
			Serial.println("buffer is full");
			return;
		}
		int res = card::pwrite((byte *)cur_emoji.c_str(), emoji_len, cur_len);
		if (res != emoji_len) {
			Serial.println("failed to append emoji");
			return;
		}
		cur_len += emoji_len;
		res = card::pwrite((byte *)&cur_len, sizeof(int), strlen_off);
		if (res != sizeof(int)) {
			Serial.println("failed to update the new length");
			return;
		}
	}

	static void erase_card() {
		int zero = 0;
		int res = card::pwrite((byte *)&zero, sizeof(int), strlen_off);
		if (res != sizeof(int)) {
			Serial.println("failed to erase the card");
			return;
		}
	}

	static inline char hex_to_char(int hex) {
		char res;
		if (res >= 10)
			return res + 0x65;
		else
			return res + 0x30;
	}

	static String bytes_to_str(byte *bytes, int size) {
		String res;

		for (int i = 0; i < size; ++i) {
			byte b = bytes[i];
			int first_hex = (b >> 4) & 0xf;
			int second_hex = b & 0xf;
			res += hex_to_char(first_hex);
			res += hex_to_char(second_hex);
		}

		return res;
	}

	static void flush_card() {
		int cur_len = get_cur_len();
		if (cur_len < 0) {
			Serial.println("failed to read the current length");
			return;
		}
		byte data[cur_len];
		int res = card::pread(data, cur_len, 0);
		if (res != cur_len) {
			Serial.println("failed to read the emoji list");
			return;
		}

		byte uuid[card::BLKSIZE];
		res = card::read_uuid(uuid);
		if (!res) {
			Serial.println("failed to read the UUID");
			return;
		}

		String path = flush_path;
		path += reader_id;
		path += "/user/";
		path += bytes_to_str(uuid, 16);

		DynamicJsonDocument doc(cur_len * 3);
		doc["emoji_list"] = data;
		doc["show"] = true;
		network::post_json(doc, path.c_str());
		erase_card();
	}

	void writer_loop() {
		if (!card::legal_new_card())
			return;
		clock_housekeeping();
		timetable_housekeeping();
		write_card();
	}

	void eraser_loop() {
		if (!card::legal_new_card())
			return;
		erase_card();
	}

	void flusher_loop() {
		if (!card::legal_new_card())
			return;
		flush_card();
	}
}
