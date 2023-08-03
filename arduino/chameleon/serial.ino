namespace serial {
	void setup() {
		Serial.begin(9600);
	}

	byte read() {
		while (!Serial.available());
		return Serial.read();
	}

	bool read(byte *dst, int len) {
		int i;
		byte recv;

		for (i = 0; i < len; ++i) {
			recv = read();
			if (recv == -1)
				return false;
			dst[i] = recv;
		}

		return read() == '\n';
	}

	String readline() {
		String res;
		char recv;
		do {
			recv = read();
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

	void write(const String &data) {
		Serial.print(data);
	}

	void write(const char *data) {
		Serial.print(data);
	}

	void write(const char data) {
		Serial.print(data);
	}

	void write(const byte *data, int len) {
		Serial.write(data, len);
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

	void accept(const String &msg) {
		Serial.print('O');
		Serial.print(msg);
		Serial.print('\n');
	}

	void accept(const byte *data, int len) {
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