#ifndef _BUZZ_H
#define _BUZZ_H

#include "config.h"

namespace buzz {
#ifdef D1R1
#error "TODO; define the IO pin in buzz.h"
#elif defined D1R2
	const int IO_PIN = D3;
#else
#error "define the board type in master_config.h"
#endif
	void setup();	
	void beep();
	void bad_beep();
}

#endif