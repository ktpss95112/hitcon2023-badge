#ifndef _CRYPTO_H
#define _CRYPTO_H

#include "card.h"

namespace crypto {
	const int data_off = 272;
	const int hmac_off = data_off + card::BLKSIZE;

	void setup();
	void process_card();
}

#endif