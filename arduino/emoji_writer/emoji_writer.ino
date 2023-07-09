#include "wifi.h"
#include "card.h"
#include "game.h"

/*
 * Game Configuration
 */
#define MAX_DATA 204

/*
 * Entrypoints
 */
void setup() {
	Serial.begin(9600);
	wifi::setup();
	card::setup();
	game::setup();
}

void loop() {
	game::writer_loop();
}
