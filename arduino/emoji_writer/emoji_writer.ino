#include "wifi.h"
#include "card.h"

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
}

void loop() {
	if (!card::legal_new_card())
		return;
}
