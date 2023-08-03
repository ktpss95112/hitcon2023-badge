#ifndef _LCD_H
#define _LCD_H

#include <LiquidCrystal_I2C.h>

namespace lcd {
	static const int NROW = 2;
	static const int NCOL = 16;

	LiquidCrystal_I2C lcd(0x27,16,2);

	uint8_t custom_chars[][8] {
		{
			0b00000,
			0b01010,
			0b11111,
			0b11111,
			0b01110,
			0b00100,
			0b00000,
			0b00000
		}
	};

	void setup();
	bool print(int row, const String &msg);
	bool print(int row, const char *msg);
	bool clear(int row);
	bool write(int chr);
	bool set_cursor(int row, int col);
}

#endif