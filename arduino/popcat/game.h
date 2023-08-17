#ifndef _GAME_H
#define _GAME_H

#include "card.h"
#include "config.h"

namespace game {
    const char *incr_path = "/tap/popcat/" GAME_READER_ID;
    const int day1_incr_off = 20 * card::BLKSIZE;
    const int day2_incr_off = day1_incr_off + sizeof(int);
    const int err_off = day2_incr_off + sizeof(int);
    const int incr_off[] = {err_off, day1_incr_off, day2_incr_off};
    void setup();
    bool process_card();
}

#endif
