#include "network.h"
#include "crypto.h"
#include "card.h"
#include "lcd.h"
#include "buzz.h"

void setup() {
	Serial.begin(9600);
	// foolproof
	Serial.print("\n");
	Serial.println("reader type = crypto");
	Serial.println("reader id = " GAME_READER_ID);

	lcd::setup();
    lcd::print_multi("Initialising\n...");
    network::setup();
	card::setup();
	crypto::setup();
    buzz::beep();
    lcd::clear();
}

void loop() {
	bool res;

	if (!card::legal_new_card())
		return;

	lcd::print_multi("Processing...\nDon't move");
	res = crypto::process_card();
	card::done();

	if (res) {
		lcd::clear();
		lcd::print_multi("Success");
		buzz::beep();
	} else {
		lcd::clear();
		lcd::print_multi("Fail");
		buzz::bad_beep();
	}
	delay(2000);
	lcd::clear();
}
