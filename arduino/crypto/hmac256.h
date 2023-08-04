#ifndef _HMAC_H
#define _HMAC_H

#include "config.h"

namespace hmac256 {
	const byte hmac_key[] = GAME_HMAC_KEY;
	const int HMACSIZE = 32;
	bool verify_hmac(byte *data, int len, byte *expected);
	void gen_hmac(byte *data, int len, byte *dest);
}

#endif