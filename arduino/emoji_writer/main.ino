#include "network.h"
#include "card.h"
#include "emoji_writer.h"
#include "buzz.h"
#include "lcd.h"

/*
 * Entrypoints
 */
void setup() {
	Serial.begin(9600);
	lcd::setup();
	lcd::print_multi("Initialising\n...");
	network::setup();
	card::setup();
	emoji_writer::setup();
	buzz::beep();
	lcd::clear();
}

void loop() {
	if (!card::legal_new_card())
		return;

	if (emoji_writer::process_card())
		buzz::beep();
	else
		buzz::bad_beep();
	card::done();
}
