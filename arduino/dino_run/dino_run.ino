#include "card.h"

/*
 * Entrypoints
 */
void setup() {
	Serial.begin(9600);
	card::setup();
}

void loop() {
	delay(100);
	if (!card::legal_new_card())
		return;
	Serial.println("1");
}