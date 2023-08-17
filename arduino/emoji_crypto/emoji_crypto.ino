#include "crypto.h"
#include "card.h"
#include "network.h"
#include "emoji_writer.h"
#include "lcd.h"
#include "buzz.h"

void setup() {
	Serial.begin(9600);
	lcd::setup();
	lcd::print_multi("Initialising\n...");
	card::setup();
	network::setup();
	emoji_writer::setup();
	crypto::setup();
	buzz::beep();
	lcd::clear();
}

void loop() {
	bool res;
	if (!card::legal_new_card())
		return;

	lcd::print_multi("Processing...\nDon't move");
	crypto::process_card();
	res = emoji_writer::process_card();
	card::done();

	if (res)
		buzz::beep();
	else
		buzz::bad_beep();
	delay(2000);
	lcd::clear();
}
