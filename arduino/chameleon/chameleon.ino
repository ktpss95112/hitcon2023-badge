#include "config.h"
#include "card.h"
#include "serial.h"

void setup() {
	serial::setup();
	card::setup();
}

/*
 * Initialize the card reader.
 */
void initialize() {
	card::done();
	serial::init();
}

/*
 * Check whether the block ID is valid.
 */
bool valid_block(int blkid) {
	return blkid >= 0 && blkid < card::BLKCNT;
}

/*
 * Read a block from the card.
 */
void read_block(int blkid) {
	static const String no_card = "card not found or invalid";
	static const String bad_id = "invalid block ID ";
	static const String card_err = "error while reading from card";
	byte buf[card::BLKSIZE];

	if (!valid_block(blkid)) {
		serial::error(bad_id + blkid);
		return;
	}

	if (!card::reset()) {
		serial::error(no_card);
		return;
	}

	if (card::read_block(buf, blkid))
		serial::accept_with_data(buf, sizeof(buf));
	else
		serial::error(card_err);
}

void write_block(int blkid) {
	static const String no_card = "card not found or invalid";
	static const String bad_id = "invalid block ID ";
	static const String serial_err = "error while reading from serial";
	static const String card_err = "error while writing to card";
	byte buf[card::BLKSIZE];

	if (!serial::read(buf, sizeof(buf))) {
		serial::error(serial_err);
		return;
	}

	if (!valid_block(blkid)) {
		serial::error(bad_id + blkid);
		return;
	}

	if (!card::reset()) {
		serial::error(no_card);
		return;
	}

	if (card::write_block(buf, blkid))
		serial::accept();
	else
		serial::error(card_err);
}

void write_uid() {
	static const String no_card = "card not found or invalid";
	static const String serial_err = "error while reading from serial";
	static const String card_err = "error while writing to card";
	byte buf[card::UIDSIZE];

	if (!serial::read(buf, sizeof(buf))) {
		serial::error(serial_err);
		return;
	}

	if (!card::reset()) {
		serial::error(no_card);
		return;
	}

	if (card::write_uid(buf))
		serial::accept();
	else
		serial::error(card_err);
}

void read_uid() {
	static const String no_card = "card not found or invalid";
	byte buf[card::UIDSIZE];

	if (!card::reset()) {
		serial::error(no_card);
		return;
	}

	card::read_uid(buf);
	serial::accept_with_data(buf, sizeof(buf));
}

void loop() {
	String command = serial::readline();
	if (command == "INIT")
		initialize();
	else if (command == "READ")
		read_block(serial::read_int());
	else if (command == "WRITE")
		write_block(serial::read_int());
	else if (command == "READ_UID")
		read_uid();
	else if (command == "WRITE_UID")
		write_uid();
	else
		serial::error(bad_command + command)
}
