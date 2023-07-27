namespace util {
	static inline char hex_to_char(int hex) {
		if (hex >= 10)
			return hex - 10 + 0x41;
		else
			return hex + 0x30;
	}

	String bytes_to_str(byte *bytes, int size) {
		String res;

		for (int i = 0; i < size; ++i) {
			byte b = bytes[i];
			int first_hex = (b >> 4) & 0xf;
			int second_hex = b & 0xf;
			res += hex_to_char(first_hex);
			res += hex_to_char(second_hex);
		}

		return res;
	}
}