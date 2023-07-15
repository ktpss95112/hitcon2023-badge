#include "network.h"
#include "card.h"
#include "game.h"
#include "config.h"

/*
 * Entrypoints
 */
void setup() {
	Serial.begin(9600);
	network::setup();
	card::setup();
	game::setup();
}

void loop() {
#ifdef WRITER
	game::writer_loop();
#elif defined ERASER
	game::eraser_loop();
#elif defined FLUSHER
	game::flusher_loop();
#endif
}
