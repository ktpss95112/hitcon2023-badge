#include "lcd.h"

#include "lcd.h"

void setup() {
	String msg = "xyz";
	lcd::setup();
	lcd::print(0, "aoeu");
	delay(3000);
	lcd::clear(0);
	lcd::print(0, msg);
	lcd::write(0);
}

void loop() {
}