namespace serial {
	void setup();
	String readline();
	void init();
	bool read(byte *dst, int len);
	void debug(const String &msg);
	void debug(const char *msg);
	void accept();
	void accept_with_data(const byte *data, int len);
	void error(const String &msg);
	void error(const char *msg);
	int read_int();
}