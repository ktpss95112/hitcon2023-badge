#include "card.h"

/*
 * Entrypoints
 */
bool readid_flag = false;
byte idbuf[18];
void setup() {
	Serial.begin(9600);
	card::setup();
}

void loop() {
  delay(50);
  card::read_uuid(idbuf);
	if (!card::legal_new_card())
		return;
  if (!card::read_uuid(idbuf))
    return;
  for(int i=0;i<8;i++)
    Serial.printf("%02x", idbuf[i]);
  Serial.println("");
}