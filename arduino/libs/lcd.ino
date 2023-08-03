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

	static inline valid_col(int col) {
		return col >= 0 && col < NCOL;
	}

	bool print(int row, const String &msg) {
		int len;

		if (!valid_row(row))
			return false;

		len = msg.length();
		if (len > NCOL)
			return false;
		
		lcd.setCursor(row, 0);
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

		lcd.setCursor(row, 0);
		lcd.print(msg);

		return true;
	}

	bool clear(int row) {
		int i;

		if (!valid_row(row))
			return false;

		lcd.setCursor(row, 0);
		for (i = 0; i < NCOL; ++i)
			lcd.print(' ');

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
		
		lcd.setCursor(row, col);
	}
}