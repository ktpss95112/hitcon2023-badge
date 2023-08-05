#include "game.h"
#include "util.h"
#include "card.h"
#include "hmac256.h"
#include "lcd.h"

namespace game {
	static int update_data(int data) {
		return data + 1;
	}

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
		succ_msg += data;
		lcd::clear();
		lcd::print_multi(succ_msg.c_str(), LCD_DELAY);
		Serial.printf("data is now %d", data);
		Serial.println();
	}
}