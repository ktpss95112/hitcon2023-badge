#ifndef _CRYPTO_H
#define _CRYPTO_H

#include "card.h"

namespace crypto {
	const int data_off = 272;
	const int hmac_off = data_off + card::BLKSIZE;

	const char *tap_record_path = "/tap/crypto/";

	void setup();
	bool process_card();
}

#endif