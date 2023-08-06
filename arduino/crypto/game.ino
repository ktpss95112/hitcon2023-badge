#include "game.h"
#include "util.h"
#include "card.h"
#include "hmac256.h"
#include "config.h"

namespace game {
	void setup() {
		randomSeed(RANDOM_SEED);
	}

#ifdef DEVCORE
	static uint32_t update_data(uint32_t src) {
		static char str[] = "DVCR";
		return src ^ *(int *)str;
	}
#elif defined CYCRAFT
	static uint32_t update_data(uint32_t src) {
		static char str[] = "CRFT";
		return src ^ *(int *)str;
	}
#elif defined FOXCONN
	static uint32_t update_data(uint32_t src) {
		static char str[] = "2317";
		return src ^ *(int *)str;
	}
#elif defined ISIP
	static uint32_t update_data(uint32_t src) {
		static char str[] = "ISIP";
		return src ^ *(int *)str;
	}
#elif defined KLICKLACK
	static uint32_t update_data(uint32_t src) {
		static char str[] = "KKCO";
		return src ^ *(int *)str;
	}
#elif defined CHT_SEC
	static uint32_t update_data(uint32_t src) {
		static char str[] = "CHTS";
		return src ^ *(int *)str;
	}
#elif defined TRAPA
	static uint32_t update_data(uint32_t src) {
		static char str[] = "TRPA";
		return src ^ *(int *)str;
	}
#elif defined RAKUTEN
	static uint32_t update_data(uint32_t src) {
		static char str[] = "RKTN";
		return src ^ *(int *)str;
	}
#elif defined KKCOMPANY
	static uint32_t update_data(uint32_t src) {
		static char str[] = "KBOX";
		return src ^ *(int *)str;
	}
#elif defined OFFSEC
	static uint32_t update_data(uint32_t src) {
		static char str[] = "OFSC";
		return src ^ *(int *)str;
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

#ifndef RESET
		if (!hmac256::verify_hmac((byte *)&data, sizeof(data), uid, hmac)) {
			Serial.println("HMAC verification failed");
			return;
		}
#endif

		data = update_data(data);
		hmac256::gen_hmac((byte *)&data, sizeof(data), uid, hmac);

		if (card::pwrite((byte *)&data, sizeof(data), data_off) != sizeof(data)) {
			Serial.println("Failed writing the data to card");
			return;
		}

		if (card::pwrite(hmac, sizeof(hmac), hmac_off) != sizeof(hmac)) {
			Serial.println("Failed writing the HMAC to card");
			return;
		}

		succ_msg = "updated data:\n";
		succ_msg += String(data, HEX);
		Serial.printf("data is now %x", data);
		Serial.println();
	}
}