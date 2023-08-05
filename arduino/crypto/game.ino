#include "game.h"
#include "util.h"
#include "card.h"
#include "hmac256.h"

namespace game {
	static int update_data(int data) {
		return data + 1;
	}

	void process_card() {
		byte hmac[hmac256::HMACSIZE];
		byte uid[card::UIDSIZE];
		int data;

		if (card::pread((byte *)&data, sizeof(data), data_off) != sizeof(data)) {
			Serial.println("Failed reading the data from card");
			return;
		}

		if (card::pread(hmac, sizeof(hmac), hmac_off) != sizeof(hmac)) {
			Serial.println("Failed reading the hmac from card");
			return;
		}

		if (!card::read_uid(uid)) {
			Serial.println("Failed reading the UID from card");
			return;
		}

		if (!hmac256::verify_hmac((byte *)&data, sizeof(data), uid, hmac)) {
			Serial.println("HMAC verification failed");
			return;
		}

		data = update_data(data);
		hmac256::gen_hmac((byte *)&data, sizeof(data), uid, hmac);

		if (card::pwrite((byte *)&data, sizeof(data), data_off) != sizeof(data)) {
			Serial.println("Failed writing the data to card");
			return;
		}

		if (card::pwrite(hmac, sizeof(hmac), hmac_off) != sizeof(hmac)) {
			Serial.println("Failed writing the hash to card");
			return;
		}

		Serial.printf("data is now %d", data);
		Serial.println();
	}
}