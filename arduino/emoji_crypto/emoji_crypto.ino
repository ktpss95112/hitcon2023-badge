#include "crypto.h"
#include "card.h"
#include "network.h"
#include "emoji_writer.h"
#include "lcd.h"
#include "buzz.h"

void setup() {
	Serial.begin(9600);
	// foolproof
	Serial.print("\n");
	Serial.println("reader type = emoji_crypto");
	Serial.println("reader id = " GAME_READER_ID);

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
	if (!card::legal_new_card())
		return;

	lcd::print_multi("Processing...\nDon't move card");

	bool res1 = crypto::process_card(false);
	bool res2 = emoji_writer::process_card();
	card::done();

	if (res1 && res2) {
		lcd::print_multi("Success!");
		buzz::beep();
	} else if (!res1 && res2) {
		lcd::print_multi("crypto success\nemoji fail");
		buzz::bad_beep();
	} else if (res1 && !res2) {
		lcd::print_multi("crypto fail\nemoji success");
		buzz::bad_beep();
	} else {
		lcd::print_multi("crypto and\nemoji fail");
		buzz::bad_beep();
	}
	delay(2000);
	lcd::clear();
}
