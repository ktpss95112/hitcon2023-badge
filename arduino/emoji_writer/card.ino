namespace card {
	void setup() {
		Serial.println(F("Setting up mfrc522..."));
		SPI.begin();
		mfrc522.PCD_Init();
	
		for (byte i = 0; i < 6; ++i)
			default_key.keyByte[i] = 0xff;
		Serial.println(F("Done."));
	}

	bool legal_new_card() {
		if (!mfrc522.PICC_IsNewCardPresent())
			return false;
		if (!mfrc522.PICC_ReadCardSerial())
			return false;

		MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
		if (piccType != MFRC522::PICC_TYPE_MIFARE_MINI &&
			piccType != MFRC522::PICC_TYPE_MIFARE_1K &&
			piccType != MFRC522::PICC_TYPE_MIFARE_4K)
			return false;

		return true;
	}

	/*
	 * A sector has two keys: A and B.
	 * Typically A is RO and B is RW.
	 */
	static bool auth_b(byte blockaddr) {
		MFRC522::StatusCode status;
		status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_B, blockaddr, &default_key, &mfrc522.uid);
		return status == MFRC522::STATUS_OK;
	}

	/*
	 * Maps logical offset to block address.
	 */
	static int get_blockaddr(int offset) {
		int block_untrans = offset / BLKSIZE;
		if (block_untrans <= 1)
			return block_untrans + 1;
		block_untrans -= 2;
		return 4 * (block_untrans/3+1) + block_untrans%3;
	}
	
	/*
	 * Maps logical offset to block offset.
	 */
	static int get_blockoff(int offset) {
		return offset % BLKSIZE;
	}

	/*
	 * Read the `blockaddr`-th block, and copy `nbyte` bytes to `buf`
	 * starting from the `from`-th one.
	 * Assumes `auth_b` is already called.
	 */
	static bool read_block(byte *buf, int blockaddr, int from, byte nbyte) {
		MFRC522::StatusCode status;
		/* 2 more bytes to store CRC-A */
		byte tmpbuf[BLKSIZE + 2];
		byte bufsz = sizeof(tmpbuf);

		status = mfrc522.MIFARE_Read(blockaddr, tmpbuf, &bufsz);
		if (status == MFRC522::STATUS_OK) {
			memcpy(buf, tmpbuf + from, nbyte);
			return true;
		}

		return false;
	}

	/*
	 * Same as `pread` in libc, but without `fildes`.
	 */
	int pread(byte *buf, int nbyte, int offset) {
		bool res;
		byte to_read;
		int blockoff;
		int blockaddr;
		int remaining = nbyte;

		while (remaining) {
			blockaddr = get_blockaddr(offset);
			blockoff = get_blockoff(offset);
			to_read = min(remaining, BLKSIZE - blockoff);

			res = auth_b(blockaddr);
			if (!res)
				break;
			res = read_block(buf, blockaddr, blockoff, to_read);
			if (!res)
				break;

			buf += to_read;
			offset += to_read;
			remaining -= to_read;
		}

		return nbyte - remaining;
	}

	/*
	 * Update `nbyte` bytes since the `from`-th in the `blockaddr`-th block.
	 * Assumes `auth_b` is already called.
	 */
	static bool write_block(byte *buf, int blockaddr, int from, int nbytes) {
		bool res;
		MFRC522::StatusCode status;
		byte tmpbuf[BLKSIZE];

		if (nbytes != BLKSIZE) {
			res = read_block(tmpbuf, blockaddr, 0, BLKSIZE);
			if (!res)
				return false;
		}

		memcpy(tmpbuf + from, buf, nbytes);

		status = mfrc522.MIFARE_Write(blockaddr, tmpbuf, sizeof(tmpbuf));
		return status == MFRC522::STATUS_OK;
	}

	int pwrite(byte *buf, int nbyte, int offset) {
		bool res;
		byte to_write;
		int blockoff;
		int blockaddr;
		int remaining = nbyte;

		while (remaining) {
			blockaddr = get_blockaddr(offset);
			blockoff = get_blockoff(offset);
			to_write = min(remaining, BLKSIZE - blockoff);

			res = auth_b(blockaddr);
			if (!res)
				break;
			res = write_block(buf, blockaddr, blockoff, to_write);
			if (!res)
				break;

			buf += to_write;
			offset += to_write;
			remaining -= to_write;
		}

		return nbyte - remaining;
	}
};
