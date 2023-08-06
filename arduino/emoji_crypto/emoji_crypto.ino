#include "crypto.h"
#include "card.h"
#include "network.h"
#include "emoji_writer.h"

void setup() {
	Serial.begin(9600);
	card::setup();
	network::setup();
	emoji_writer::setup();
	crypto::setup();
}

void loop() {
	if (!card::legal_new_card())
		return;
	crypto::process_card();
	card::reset();
	emoji_writer::loop();
	card::done();
}