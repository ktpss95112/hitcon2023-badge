#ifndef _LCD_H
#define _LCD_H

#include <LiquidCrystal_I2C.h>

namespace lcd {
	static const int NROW = 2;
	static const int NCOL = 16;

	static const int ALERT_DUR = 2000;

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
	bool print(int row, const String &msg, int duration);
	bool print(int row, const char *msg, int duration);
	bool print_multi(const char *msg);
	bool print_multi(const String &msg);
	bool print_multi(const char *msg, int duration);
	bool print_multi(const String &msg, int duration);
	bool alert_multi(const char *msg);
	bool alert_multi(const String &msg);
	bool clear();
	bool clear(int row);
	bool write(int chr);
	bool set_cursor(int row, int col);
}

#endif