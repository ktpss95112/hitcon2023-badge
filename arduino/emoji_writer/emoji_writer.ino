#include <time.h>
#include <ArduinoJson.h>
#include <ESP8266HTTPClient.h>
#include <memory>
#include "emoji_writer.h"
#include "card.h"
#include "network.h"
#include "util.h"
#include "config.h"
#include "lcd.h"

namespace emoji_writer {
	static void push_one_emoji(const JsonVariant &doc) {
		const char *starttime_str = doc[0];
		const char *emoji_str = doc[1];

		time_t starttime = util::str_to_epoch(starttime_str, "%FT%T");
		std::shared_ptr<emoji_timetable> cur(new emoji_timetable(
			starttime, emoji_str, emoji_timetable_head
		));
		Serial.println(cur->emoji);
		Serial.printf("%s", starttime_str);
		Serial.println();
		emoji_timetable_head = cur;
	}

	static void pop_one_emoji() {
		emoji_timetable_head = emoji_timetable_head->next;
	}

	static bool read_timetable() {
		int i, n, part;

		for (part = 3; part >= 0; --part) {
			DynamicJsonDocument doc(1024);
			String path = emoji_timetable_path;
			path += "/day/";
			path += network::TODAY;
			path += "/part/";
			path += part;
			Serial.println(path);
			if (!network::get_json(doc, path.c_str())) {
				return false;
			}

			n = doc.size();
			/*
			* Since the timetable in the server is in ascending order,
			* we reverse it here so the head is the earliest entry.
			*/
			for (i = n-1; i >= 0; --i)
				push_one_emoji(doc[i]);
		}
		return true;
	}

	static time_t seconds_from_boot() {
		return millis() / 1000;
	}

	static time_t estimated_cur_time() {
		return clock_offset + seconds_from_boot();
	}

	static bool sync_clock() {
		time_t now = network::fetch_time();
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
		if (!sync_clock()) {
			lcd::print_multi("clock error\ncontact staff");
			Serial.println("clock synchronization failed");
			return;
		}
#ifdef WRITER
		if (!read_timetable()) {
			lcd::print_multi("network error\ncontact staff");
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

	static bool write_card() {
		int cur_len = get_cur_len();
		if (cur_len < 0) {
			Serial.println("failed to read the current length");
			lcd::print_multi("card error\ncontact staff");
			return false;
		}
		Serial.printf("current len: %d", cur_len);
		Serial.println();

		String &cur_emoji = emoji_timetable_head->emoji;
		int emoji_len = cur_emoji.length();
		if (cur_len + emoji_len >= capacity) {
			Serial.println("buffer is full");
			lcd::print_multi("buffer full\nflush first");
			return false;
		}
		int res = card::pwrite((byte *)cur_emoji.c_str(), emoji_len, cur_len);
		if (res != emoji_len) {
			Serial.println("failed to append emoji");
			lcd::print_multi("card error\ncontact staff");
			return false;
		}
		cur_len += emoji_len;
		res = card::pwrite((byte *)&cur_len, sizeof(int), strlen_off);
		if (res != sizeof(int)) {
			Serial.println("failed to update the new length");
			lcd::print_multi("card error\ncontact staff");
			return false;
		}

		Serial.println("about to write card");
		return true;
	}

	static bool erase_card() {
		int zero = 0;
		int res = card::pwrite((byte *)&zero, sizeof(int), strlen_off);
		if (res != sizeof(int)) {
			Serial.println("failed to erase the card");
			lcd::print_multi("card error\ncontact staff");
			return false;
		}
		Serial.println("erase successful");
		return true;
	}

	static bool flush_card() {
		byte data[capacity];
		int cur_len = get_cur_len();
		if (cur_len < 0) {
			Serial.println("failed to read the current length");
			lcd::print_multi("card error\ncontact staff");
			return false;
		} else if (cur_len == 0) {
			Serial.println("cur_len is 0, nothing to flush");
			lcd::print_multi("Empty buffer,\nflush nothing");
			return false;
		}
		Serial.printf("length: %d", cur_len);
		Serial.println();

		int res = card::pread(data, cur_len, 0);
		if (res != cur_len) {
			Serial.println("failed to read the emoji list");
			lcd::print_multi("card error\ncontact staff");
			return false;
		}
		data[cur_len] = '\0';
		Serial.printf("data:");
		for (int i = 0; i < cur_len; ++i)
			Serial.printf("%c", data[i]);
		Serial.println();

		byte uid[card::UIDSIZE];
		res = card::read_uid(uid);
		if (!res) {
			Serial.println("failed to read the UID");
			lcd::print_multi("card error\ncontact staff");
			return false;
		}

		String path = flush_path;
		path += reader_id;
		path += "/user/";
		path += util::bytes_to_str(uid, card::UIDSIZE);
		Serial.println("uid:");
		Serial.println(util::bytes_to_str(uid, card::UIDSIZE));

		/* The *3 is just an approximation. */
		DynamicJsonDocument doc(5*cur_len+30);
		doc["emoji_list"] = String((char *)data);
		doc["show"] = true;
		if (!network::post_json(doc, path.c_str())) {
			Serial.println("failed to post the emoji");
			lcd::print_multi("network error\ncontact staff");
			return false;
		}

		if (!erase_card()) {
			Serial.println("failed to erase card");
			lcd::print_multi("card error\ncontact staff");
			return false;
		}

		Serial.println("success on flushing emoji buffer");
		lcd::print_multi("Success");
		return true;
	}

	static bool writer_process() {
		bool res;

		clock_housekeeping();
		timetable_housekeeping();
		res = write_card();
		card::done();

		if (!res) {
			return false;
		}

		// record tap
		byte uid[card::UIDSIZE];
		res = card::read_uid(uid);
		if (!res) {
			Serial.println("failed to read the UID");
			lcd::print_multi("card error\ncontact staff");
			return false;
		}

		// true / false only
		DynamicJsonDocument doc(0x10);
		String path = tap_record_path;
		path += reader_id;
		path += "/user/";
		path += util::bytes_to_str(uid, card::UIDSIZE);
		return network::post_json(doc, path.c_str());
	}

	static bool eraser_process() {
		bool res;
		res = erase_card();
		card::done();
		return res;
	}

	static bool flusher_process() {
		bool res;
		res = flush_card();
		card::done();
		return res;
	}

	bool process_card() {
		bool res;
#ifdef WRITER
		res = writer_process();
#elif defined ERASER
		res = eraser_process();
#elif defined FLUSHER
		res = flusher_process();
#else
#error "please specify the card reader type"
#endif
		return res;
	}
}
