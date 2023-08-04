#ifndef _GAME_H
#define _GAME_H

#include "card.h"

namespace game {
	const int data_off = 272;
	const int hmac_off = data_off + card::BLKSIZE;

	void process_card();
}

#endif