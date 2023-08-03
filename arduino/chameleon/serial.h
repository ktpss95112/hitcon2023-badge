namespace serial {
	void setup();
	String readline();
	void init();
    bool read(byte *dst, int len);
	void write(const String &data);
	void write(const char *data);
	void write(const char data);
	void write(const byte *data, int len);
	void debug(const String &msg);
	void debug(const char *msg);
    void accept();
	void accept(const String &msg);
	void accept(const byte *data, int len);
	void error(const String &msg);
	void error(const char *msg);
	int read_int();
}