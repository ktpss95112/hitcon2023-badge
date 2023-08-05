#include <SHA256.h>
#include "hmac256.h"
#include "card.h"

namespace hmac256 {
	static bool arr_eq(const byte *a, const byte *b, int len) {
		for (int i = 0; i < len; ++i) {
			if (a[i] != b[i])
				return false;
		}

		return true;
	}
	bool verify_hmac(byte *data, int len, byte *uid, byte *expected) {
		byte hmac[HMACSIZE];
		gen_hmac(data, len, uid, hmac);
		return arr_eq(hmac, expected, HMACSIZE);
	}

	void gen_hmac(byte *data, int len, byte *uid, byte *dest) {
		SHA256 hash;
		hash.resetHMAC(hmac_key, sizeof(hmac_key));
		hash.update(uid, card::UIDSIZE);
		hash.update(data, len);
		hash.finalizeHMAC(hmac_key, sizeof(hmac_key), dest, HMACSIZE);
	}
}