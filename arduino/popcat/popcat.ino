#include "network.h"
#include "card.h"
#include "game.h"

void setup() {
    Serial.begin(9600);
    network::setup();
    card::setup();
    game::setup();
}

void loop() {
    if (!card::legal_new_card())
        return;
    game::process_card();
    card::done();
}