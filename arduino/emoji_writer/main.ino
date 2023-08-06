#include "network.h"
#include "card.h"
#include "emoji_writer.h"

/*
 * Entrypoints
 */
void setup() {
	Serial.begin(9600);
	network::setup();
	card::setup();
	emoji_writer::setup();
}

void loop() {
	emoji_writer::loop();
}
