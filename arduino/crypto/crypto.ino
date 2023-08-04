#include "game.h"
#include "card.h"

void setup() {
	Serial.begin(9600);
	card::setup();
}

void loop() {
	if (!card::legal_new_card())
		return;
	game::process_card();
	card::done();
}