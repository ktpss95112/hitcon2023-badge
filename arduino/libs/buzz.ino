#include "buzz.h"
namespace buzz {
	void setup() {
	}

	void beep() {
		tone(IO_PIN, 440, 250);
		delay(250);
		noTone(IO_PIN);
		delay(250);
	}

	void bad_beep() {
		tone(IO_PIN, 162, 250);
		delay(250);
		noTone(IO_PIN);
		delay(250);
	}
}