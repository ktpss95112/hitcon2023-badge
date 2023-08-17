#ifndef _CARD_H
#define _CARD_H

#include <SPI.h>
#include <MFRC522.h>
#include "config.h"

namespace card {
#ifdef D1R1
	const auto RST_PIN = D9;
	const auto SS_PIN = D10;
#elif defined D1R2
	const auto RST_PIN = D4;
	const auto SS_PIN = D8;
#else
#error "please specify the board type in master_config.h"
#endif
	const int BLKSIZE = 16;
	const int UIDSIZE = 4;
	const int BLKCNT = 64;

	MFRC522 mfrc522(SS_PIN, RST_PIN);
	MFRC522::MIFARE_Key default_key;
	void setup();
	bool legal_new_card();
	bool read_block(byte *buf, int blockaddr);
	bool write_block(byte *buf, int blockaddr);
	int pread(byte *buf, int nbyte, int offset);
	int pwrite(byte *buf, int nbyte, int offset);
	bool read_uid(byte *buf);
	bool write_uid(byte *buf);
	void done();
	bool reset();
}

#endif
