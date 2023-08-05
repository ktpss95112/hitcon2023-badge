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

#ifdef SPONSOR1
	static uint32_t update_data(uint32_t src) {
		uint8_t x[4];
		x[0] = src & 0xFF;
		x[1] = (src >> 8) & 0xFF;
		x[2] = (src >> 16) & 0xFF;
		x[3] = (src >> 24) & 0xFF;

		static const uint8_t mat[4][4] {
			{137, 172, 56, 176},
			{171, 119, 211, 146},
			{183, 240, 17, 44},
			{119, 8, 55, 237}
		};
		uint8_t res[4];
		for (int i = 0; i < 4; i++) {
			uint32_t accu = 0;
			for (int j = 0; j < 4; j++) {
				accu += ((uint32_t)mat[i][j])*((uint32_t)x[j]);
			}
			res[i] = accu & 0xFF;
		}

		return res[0] | (res[1] << 8) | (res[2] << 16) | (res[3] << 24);
	}
#elif defined SPONSOR2
	static uint32_t update_data(uint32_t src) {
		return ((uint64_t)src) * 3300963383 % 3398445031;
	}
#elif defined SPONSOR3
	static uint32_t pow(uint32_t x, uint32_t n) {
		if (n == 0)
			return 1;
		uint32_t p = pow(x, n / 2);
		if (n % 2)
			return x * p * p;
		else
			return p * p;
	}
	static uint32_t update_data(uint32_t src) {
		return (x != 0) ? pow(x, x) : 0;
	}
#elif defined WILD1
	static uint32_t update_data(uint32_t src) {
		return 0;
	}
#elif defined WILD2
	static uint32_t update_data(uint32_t src) {
		return src + 1;
	}
#elif defined WILD3
	static uint32_t update_data(uint32_t src) {
		uint32_t r = src & 0b11111;
		uint32_t mask_r = (0xffffffff >> r) << r;
		uint32_t mask_another = ~mask_r;
		return ((src & mask_r) >> r) | ((src & mask_another) << (32-r));
	}
#elif defined WILD4
	static uint32_t update_data(uint32_t src) {
		return ((src & 0xffff0000) >> 16) | ((src & 0xffff) << 16);
	}
#elif defined WILD5
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

		if (!hmac256::verify_hmac((byte *)&data, sizeof(data), uid, hmac)) {
			Serial.println("HMAC verification failed");
			lcd::clear();
			lcd::print_multi("invalid HMAC\ncontact staff", LCD_DELAY);
			return;
		}

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