#ifndef _GAME_H
#define _GAME_H

#include "card.h"
#include "config.h"

namespace game {
    int TODAY;
    const int DAY2_EPOCH = 1692374400;
    const char *incr_path = "/tap/popcat/" GAME_READER_ID;
    const int raw_incr_off = 20 * card::BLKSIZE;
    const int xor_incr_off = raw_incr_off + sizeof(int);
    const int incr_off[] = {raw_incr_off, xor_incr_off};
    void setup();
    void process_card();
}

#endif