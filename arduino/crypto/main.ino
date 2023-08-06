#include "crypto.h"
#include "card.h"

void setup() {
	Serial.begin(9600);
	card::setup();
	crypto::setup();
}

void loop() {
	if (!card::legal_new_card())
		return;
	crypto::process_card();
	card::done();
}