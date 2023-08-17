#include "crypto.h"
#include "card.h"
#include "lcd.h"
#include "buzz.h"

void setup() {
	Serial.begin(9600);
	lcd::setup();
	card::setup();
	crypto::setup();
}

void loop() {
	bool res;

	if (!card::legal_new_card())
		return;
	
	lcd::print_multi("Processing...\nDon't move");
	res = crypto::process_card();
	card::done();

	if (res)
		buzz::beep();
	else
		buzz::bad_beep();
	
	delay(2000);
	lcd::clear();
}