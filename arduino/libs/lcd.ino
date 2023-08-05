#include "lcd.h"

namespace lcd {
	static void create_custom_chars() {
		int i = 0;
		
		for (uint8_t (&chr)[8]: custom_chars) {
			lcd.createChar(i, chr);
			++i;
		}
	}

	void setup() {
		lcd.init();
		lcd.clear();         
		lcd.backlight();
		create_custom_chars();
	}


	static inline bool valid_row(int row) {
		return row >= 0 && row < NROW;
	}

	static inline bool valid_col(int col) {
		return col >= 0 && col < NCOL;
	}

	bool print(int row, const String &msg) {
		int len;

		if (!valid_row(row))
			return false;

		len = msg.length();
		if (len > NCOL)
			return false;
		
		lcd.setCursor(0, row);
		lcd.print(msg);
		return true;
	}

	bool print(int row, const char *msg) {
		int len;

		if (!valid_row(row))
			return false;

		len = strlen(msg);
		if (len > NCOL)
			return false;

		lcd.setCursor(0, row);
		lcd.print(msg);

		return true;
	}

	bool print(int row, const String &msg, int duration) {
		if (!print(row, msg))
			return false;
		delay(duration);
		clear(row);
		return true;
	}

	bool print(int row, const char *msg, int duration) {
		if (!print(row, msg))
			return false;
		delay(duration);
		clear(row);
		return true;
	}

	bool print_multi(const char *msg) {
		String line;
		const int n = strlen(msg);

		for (int i = 0; i < n; ++i) {
			if (msg[i] == '\n')
				break;
			line += msg[i];
		}

		const int n1 = line.length(), n2 = n - n1 - 1;

		if (n1 == n)
			return false;
		if (n1 > NCOL)
			return false;
		if (n2 > NCOL)
			return false;

		print(0, line);
		print(1, msg + line.length() + 1);

		return true;
	}

	bool print_multi(const String &msg) {
		return print_multi(msg.c_str());
	}

	bool print_multi(const char *msg, int duration) {
		if (!print_multi(msg))
			return false;
		delay(duration);
		clear();
		return true;
	}

	bool print_multi(const String &msg, int duration) {
		return print_multi(msg.c_str(), duration);
	}

	bool clear(int row) {
		int i;

		if (!valid_row(row))
			return false;

		lcd.setCursor(0, row);
		for (i = 0; i < NCOL; ++i)
			lcd.print(' ');

		return true;
	}

	bool clear() {
		clear(0);
		clear(1);
		return true;
	}

	bool write(int chr) {
		lcd.write(chr);
		return true;
	}

	bool set_cursor(int row, int col) {
		if (!valid_row(row))
			return false;
		if (!valid_col(col))
			return false;
		
		lcd.setCursor(col, row);
		return true;
	}
}