#include <time.h>
#include <ArduinoJson.h>
#include <ESP8266HTTPClient.h>
#include <memory>
#include "game.h"
#include "card.h"
#include "network.h"
#include "util.h"

namespace game {
	static time_t str_to_epoch(const char *str) {
		tm datetime {0};
		strptime(str, "\"%FT%T.", &datetime);
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
		Serial.println(cur->emoji);
		Serial.printf("%s", starttime_str);
		Serial.println();
	}

	static void pop_one_emoji() {
		emoji_timetable_head = emoji_timetable_head->next;
	}

	static bool read_timetable() {
		int i, n;
		DynamicJsonDocument doc(1024);
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
		time_t res = clock_offset + seconds_from_boot();
		return res;
	}

	static bool sync_clock() {
		String datetime_str = network::get_string(current_time_path);
		if (datetime_str.length() == 0)
			return false;
		time_t now = str_to_epoch(datetime_str.c_str());
		Serial.printf("now: %lld", now);
		Serial.println();
		clock_offset = now - seconds_from_boot();
		Serial.printf("offset: %lld", clock_offset);
		Serial.println();
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
#ifdef WRITER
		if (!sync_clock()) {
			Serial.println("clock synchronization failed");
			return;
		}
		if (!read_timetable()) {
			Serial.println("time table read failed");
			return;
		}
#endif
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
		Serial.print("current emoji: ");
		Serial.println(emoji_timetable_head->emoji);
	}

	static void write_card() {
		int cur_len = get_cur_len();
		if (cur_len < 0) {
			Serial.println("failed to read the current length");
			return;
		}
		Serial.printf("current len: %d", cur_len);
		Serial.println();

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
		Serial.println("erase successful");
	}

	static void flush_card() {
		byte data[capacity];
		int cur_len = get_cur_len();
		if (cur_len < 0) {
			Serial.println("failed to read the current length");
			return;
		}
		Serial.printf("length: %d", cur_len);
		Serial.println();

		int res = card::pread(data, cur_len, 0);
		if (res != cur_len) {
			Serial.println("failed to read the emoji list");
			return;
		}
		data[cur_len] = '\0';
		Serial.printf("data:");
		for (int i = 0; i < cur_len; ++i)
			Serial.printf("%c", data[i]);
		Serial.println();

		byte uuid[card::BLKSIZE];
		res = card::read_uuid(uuid);
		if (!res) {
			Serial.println("failed to read the UUID");
			return;
		}

		String path = flush_path;
		path += reader_id;
		path += "/user/";
		path += util::bytes_to_str(uuid, 16);
		Serial.println("uuid:");
		Serial.println(util::bytes_to_str(uuid, 16));

		/* The *3 is just an approximation. */
		DynamicJsonDocument doc(cur_len * 3);
		doc["emoji_list"] = String((char *)data);
		doc["show"] = true;
		if (!network::post_json(doc, path.c_str())) {
			Serial.println("failed to post the emoji");
			return;
		}
		erase_card();
	}

	void writer_loop() {
		if (!card::legal_new_card())
			return;
		clock_housekeeping();
		timetable_housekeeping();
		write_card();
		card::done();
	}

	void eraser_loop() {
		if (!card::legal_new_card())
			return;
		erase_card();
		card::done();
	}

	void flusher_loop() {
		if (!card::legal_new_card())
			return;
		flush_card();
		card::done();
	}
}
