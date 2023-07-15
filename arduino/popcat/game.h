#ifndef _GAME_H
#define _GAME_H

#include "config.h"

namespace game {
    const char *incr_path = "/tap/popcat/" GAME_READER_ID;
    const int incr_off = 20 * card::BLKSIZE;
    void setup();
    void process_card();
}

#endif