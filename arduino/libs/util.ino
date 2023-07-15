namespace util {
	static inline char hex_to_char(int hex) {
		char res;
		if (res >= 10)
			return res + 0x65;
		else
			return res + 0x30;
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