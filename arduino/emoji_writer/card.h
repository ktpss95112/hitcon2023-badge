#ifndef _CARD_H
#define _CARD_H

#include <SPI.h>
#include <MFRC522.h>

namespace card {
	const auto RST_PIN = D9;
	const auto SS_PIN = D10;
	const int BLKSIZE = 16;

	MFRC522 mfrc522(SS_PIN, RST_PIN);
	MFRC522::MIFARE_Key default_key;
	void setup();
	bool legal_new_card();
	int pread(byte *buf, int nbyte, int offset);
	int pwrite(byte *buf, int nbyte, int offset);
}

#endif
