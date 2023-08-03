#include "card.h"
#include "serial.h"

void setup() {
	serial::setup();
	card::setup();
}

void reset() {
	card::done();
	while (!card::legal_new_card());
	serial::init();
}

void invalid_command(String &command) {
	static const String msg = "invalid command ";
	serial::error(msg + command);
}

bool valid_block(int blkid) {
	return blkid >= 0 && blkid < card::BLKCNT;
}

void read_block(int blkid) {
	static const String no_card = "card not found or invalid";
	static const String bad_id = "invalid block ID ";
	static const String card_err = "error while reading from card";
	byte buf[card::BLKSIZE];

	if (!valid_block(blkid)) {
		serial::error(bad_id + blkid);
		return;
	}

	if (card::read_block(buf, blkid))
		serial::accept(buf, sizeof(buf));
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

	if (card::write_block(buf, blkid))
		serial::accept();
	else
		serial::error(card_err);
}

void write_uid() {
	static const String serial_err = "error while reading from serial";
	static const String card_err = "error while writing to card";
	byte buf[card::UIDSIZE];

	if (!serial::read(buf, sizeof(buf))) {
		serial::error(serial_err);
		return;
	}

	if (card::write_uid(buf))
		serial::accept();
	else
		serial::error(card_err);
}

void loop() {
	String command = serial::readline();
	if (command == "INIT")
		reset();
	else if (command == "READ")
		read_block(serial::read_int());
	else if (command == "WRITE")
		write_block(serial::read_int());
	else if (command == "WRITE_UID")
		write_uid();
	else {
		invalid_command(command);
	}
}