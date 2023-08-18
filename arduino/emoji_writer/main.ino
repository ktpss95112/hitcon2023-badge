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
	// foolproof
	Serial.print("\n");
	Serial.println("reader type = emoji_writer");
	Serial.println("reader id = " GAME_READER_ID);

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

	lcd::print_multi("Pushing emoji\nto remote ...");
	if (emoji_writer::process_card()) {
        // no need to print lcd since game::process_card does it
		buzz::beep();
	} else {
        // no need to print lcd since game::process_card does it
		buzz::bad_beep();
	}
	card::done();
	delay(2000);
	lcd::clear();
}
