#include "game.h"
#include "util.h"
#include "card.h"
#include "hmac256.h"
#include "lcd.h"
#include "config.h"

namespace game {
	void setup() {
		randomSeed(RANDOM_SEED);
	}

#ifdef DEVCORE
	static uint32_t update_data(uint32_t src) {
		return src ^ 1146504018;
	}
#elif defined CYCRAFT
	static uint32_t update_data(uint32_t src) {
		return src ^ 1129465428;
	}
#elif defined FOXCONN
	static uint32_t update_data(uint32_t src) {
		return src ^ 842215735;
	}
#elif defined ISIP
	static uint32_t update_data(uint32_t src) {
		return src ^ 1230195024;
	}
#elif defined KLICKLACK
	static uint32_t update_data(uint32_t src) {
		return src ^ 1263223631;
	}
#elif defined CHT_SEC
	static uint32_t update_data(uint32_t src) {
		return src ^ 1128813651;
	}
#elif defined TRAPA
	static uint32_t update_data(uint32_t src) {
		return src ^ 1414680641;
	}
#elif defined RAKUTEN
	static uint32_t update_data(uint32_t src) {
		return src ^ 1380668494;
	}
#elif defined KKCOMPANY
	static uint32_t update_data(uint32_t src) {
		return src ^ 1262636888;
	}
#elif defined OFFSEC
	static uint32_t update_data(uint32_t src) {
		return src ^ 1330008899;
	}
#elif defined RESET
	static uint32_t update_data(uint32_t src) {
		return 0;
	}
#elif defined ADD1
	static uint32_t update_data(uint32_t src) {
		return src + 1;
	}
#elif defined ROR
	static uint32_t update_data(uint32_t src) {
		uint32_t r = src & 0b11111;
		uint32_t mask_r = (0xffffffff >> r) << r;
		uint32_t mask_another = ~mask_r;
		return ((src & mask_r) >> r) | ((src & mask_another) << (32-r));
	}
#elif defined SWAP_HILO
	static uint32_t update_data(uint32_t src) {
		return ((src & 0xffff0000) >> 16) | ((src & 0xffff) << 16);
	}
#elif defined RAND_FLIP
	static uint32_t update_data(uint32_t src) {
		int bit1 = random(0, 32);
		int bit2 = random(0, 31);
		if (bit2 >= bit1)
			++bit2;
		uint32_t mask = (1 << bit1) | (1 << bit2);
		return src ^ mask;
	}
#else
#error "define the card reader type in config.h"
#endif

	void process_card() {
		byte hmac[hmac256::HMACSIZE];
		byte uid[card::UIDSIZE];
		int data;
		String succ_msg;

		if (card::pread((byte *)&data, sizeof(data), data_off) != sizeof(data)) {
			Serial.println("Failed reading the data from card");
			lcd::clear();
			lcd::print_multi("read data fail\ntry again", LCD_DELAY);
			return;
		}

		if (card::pread(hmac, sizeof(hmac), hmac_off) != sizeof(hmac)) {
			Serial.println("Failed reading the hmac from card");
			lcd::clear();
			lcd::print_multi("read hmac fail\ntry again", LCD_DELAY);
			return;
		}

		if (!card::read_uid(uid)) {
			Serial.println("Failed reading the UID from card");
			lcd::clear();
			lcd::print_multi("read uid fail\ntry again", LCD_DELAY);
			return;
		}

#ifndef RESET
		if (!hmac256::verify_hmac((byte *)&data, sizeof(data), uid, hmac)) {
			Serial.println("HMAC verification failed");
			lcd::clear();
			lcd::print_multi("invalid HMAC\ncontact staff", LCD_DELAY);
			return;
		}
#endif

		data = update_data(data);
		hmac256::gen_hmac((byte *)&data, sizeof(data), uid, hmac);

		if (card::pwrite((byte *)&data, sizeof(data), data_off) != sizeof(data)) {
			Serial.println("Failed writing the data to card");
			lcd::clear();
			lcd::print_multi("write data fail\ncontact staff", LCD_DELAY);
			return;
		}

		if (card::pwrite(hmac, sizeof(hmac), hmac_off) != sizeof(hmac)) {
			Serial.println("Failed writing the HMAC to card");
			lcd::clear();
			lcd::print_multi("write HMAC fail\ncontact staff", LCD_DELAY);
			return;
		}

		succ_msg = "updated data:\n";
		succ_msg += String(data, HEX);
		lcd::clear();
		lcd::print_multi(succ_msg, LCD_DELAY);
		Serial.printf("data is now %x", data);
		Serial.println();
	}
}