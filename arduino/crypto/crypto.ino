#include "game.h"
#include "card.h"
#include "lcd.h"

void setup() {
	Serial.begin(9600);
	lcd::setup();
	card::setup();
}

void loop() {
	lcd::print_multi("crypto game\nscan card");
	if (!card::legal_new_card())
		return;
	game::process_card();
	card::done();
	lcd::clear();
}