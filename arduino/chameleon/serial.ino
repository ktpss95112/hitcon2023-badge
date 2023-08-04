namespace serial {
	void setup() {
		Serial.begin(9600);
	}

	static byte read_byte() {
		while (!Serial.available());
		return Serial.read();
	}

	bool read(byte *dst, int len) {
		int i;
		byte recv;

		for (i = 0; i < len; ++i) {
			recv = read_byte();
			if (recv == -1)
				return false;
			dst[i] = recv;
		}

		return read_byte() == '\n';
	}

	String readline() {
		String res;
		char recv;
		do {
			recv = read_byte();
			if (recv == '\n')
				break;
			else
				res += recv;
		} while (true);
		return res;
	}

	void init() {
		Serial.print("I\n");
	}

	void debug(const String &msg) {
		Serial.print('D');
		Serial.print(msg);
		Serial.print('\n');
	}
	void debug(const char *msg) {
		Serial.print('D');
		Serial.print(msg);
		Serial.print('\n');
	}

	void accept() {
		Serial.print("O\n");
	}

	void accept_with_data(const byte *data, int len) {
		Serial.print('O');
		Serial.write(data, len);
		Serial.write('\n');
	}

	void error(const String &msg) {
		Serial.print('E');
		Serial.print(msg);
		Serial.print('\n');
	}

	void error(const char *msg) {
		Serial.print('E');
		Serial.print(msg);
		Serial.print('\n');
	}

	int read_int() {
		return readline().toInt();
	}
}