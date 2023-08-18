#ifndef _EMOJI_WRITER_H
#define _EMOJI_WRITER_H

#include <WiFiClientSecureBearSSL.h>
#include "config.h"
#include "card.h"


namespace emoji_writer {
	struct emoji_timetable {
		time_t starttime;
		String emoji;
		std::shared_ptr<emoji_timetable> next;
		emoji_timetable(
			time_t starttime, const char *emoji,
			std::shared_ptr<emoji_timetable> next
		) : starttime(starttime), emoji(emoji), next(next) {}
	};

	const char *reader_id = GAME_READER_ID;

	const char *emoji_timetable_path = "/cardreader/emoji_time_table/" GAME_READER_ID;
	const char *current_time_path = "/time";
	const char *flush_path = "/tap/sponsor_flush_emoji/";
	const char *tap_record_path = "/tap/sponsor/";

	const unsigned capacity = card::BLKSIZE * 14 - sizeof(unsigned);
	const unsigned strlen_off = capacity;

	time_t clock_offset = 0;
	clock_t clock_last_update = 0;
	std::shared_ptr<emoji_timetable> emoji_timetable_head = NULL;

	void setup();
	bool process_card();
}

#endif