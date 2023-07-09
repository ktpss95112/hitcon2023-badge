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
	if (!card::legal_new_card())
		return;
	game::clock_housekeeping();
	game::timetable_housekeeping();
	game::process_card();
}
