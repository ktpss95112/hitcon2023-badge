#include "network.h"
#include "card.h"
#include "game.h"
#include "buzz.h"
#include "lcd.h"

void setup() {
    Serial.begin(9600);
	// foolproof
	Serial.print("\n");
	Serial.println("reader type = popcat");
	Serial.println("reader id = " GAME_READER_ID);

    lcd::setup();
    lcd::print_multi("Initialising\n...");
    network::setup();
    card::setup();
    game::setup();
    buzz::beep();
    lcd::clear();
}

void loop() {
    bool res;

    if (!card::legal_new_card())
        return;

    lcd::print_multi("Processing...\nDon't move");
    res = game::process_card();
    card::done();

    if (res) {
        // no need to print lcd since game::process_card does it
        buzz::beep();
    } else {
        // no need to print lcd since game::process_card does it
        buzz::bad_beep();
    }
    delay(2000);
    lcd::clear();
}
