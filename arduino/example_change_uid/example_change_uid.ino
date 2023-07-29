#include "card.h"
#include "util.h"

void setup() {
	Serial.begin(9600);
	card::setup();
}

void write_uid() {
	byte uuid[] = {0xde, 0xad, 0xbe, 0xef};
	if (card::write_uid(uuid))
		Serial.println("write success");
	else
		Serial.println("write failed");
}

void loop() {
	if (!card::legal_new_card())
		return;
	write_uid();
	card::done();
}