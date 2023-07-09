#include <time.h>
#include <ArduinoJson.h>
#include <ESP8266HTTPClient.h>
#include <memory>
#include "game.h"

namespace game {
	static bool get_json(DynamicJsonDocument &doc, const char *path) {
		HTTPClient https;
		int status_code;
		DeserializationError json_error;

		if (!https.begin(wifi_client, host, host_port, path)) {
			Serial.printf("failed connecting to %s%s", host, path);
			Serial.println();
			return false;
		}

		status_code = https.GET();
		if (status_code != 200) {
			Serial.printf("status code %d", status_code);
			Serial.println();
			return false;
		}

		json_error = deserializeJson(doc, https.getStream());
		if (json_error) {
			Serial.printf(
				"can't deserialize JSON: %s",
				json_error.f_str()
			);
			Serial.println();
			return false;
		}
		return true;
	}

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
		if (!get_json(doc, emoji_timetable_path))
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
		if (!get_json(doc, current_time_path))
			return false;
		String datetime_str = doc.as<String>();
		time_t now = str_to_epoch(datetime_str.c_str());
		clock_offset = now - seconds_from_boot();
		clock_last_update = seconds_from_boot();
		return true;
	}

	void setup() {
		wifi_client.setClientRSACert(&client_cert, &client_key);
		wifi_client.setFingerprint(host_fingerprint);
		if (!sync_clock()) {
			Serial.println("clock synchronization failed");
			return;
		}
		if (!read_timetable()) {
			Serial.println("time table read failed");
			return;
		}
	}

	void clock_housekeeping() {
		if (seconds_from_boot() < clock_last_update + CLOCK_SYNC_INTERVAL)
			return;
		sync_clock();
	}

	void timetable_housekeeping() {
		while (
			emoji_timetable_head->next &&
			emoji_timetable_head->next->starttime <= estimated_cur_time()
		)
			pop_one_emoji();
	}

	void process_card() {
		int cur_len;
		int res = card::pread((byte *)&cur_len, sizeof(int), strlen_off);
		if (res != sizeof(int)) {
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
		res = card::pwrite((byte *)cur_emoji.c_str(), emoji_len, cur_len);
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
}
