from glob import glob

import pygame as pg

# view
WINDOW_CAPTION = "HITCON 2023 Dino Run"
WINDOW_SIZE = (800, 800)
ARENA_SIZE = (800, 800)
BACKGROUND_COLOR = pg.Color("black")
PLAYER_COLOR = pg.Color("green")
OBSTACLE_COLOR = pg.Color("white")
PLAYER_LINE_COLOR = {
    "move": pg.Color("lightgoldenrod"),
    "jump": pg.Color("lightgoldenrod4"),
}
PLAYER_HEIGHT, PLAYER_WIDTH = 80, 60
OBSTACLE_HEIGHT, OBSTACLE_WIDTH = 20, 20
PLAYER_JUMP_IMGS = sorted(glob("./assets/jump/*"))
PLAYER_MOVE_IMGS = sorted(glob("./assets/move/*"))

# model
FPS = 60  # frame per second
GAME_LENGTH = 30 * FPS
PLAYER_INIT_RECT = (
    200 - PLAYER_WIDTH / 2,
    ARENA_SIZE[1] - PLAYER_HEIGHT,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
)  # (left, top, width, height)
OBSTACLE_INIT_RECT = [
    (
        ARENA_SIZE[0] - 2 * OBSTACLE_WIDTH,
        ARENA_SIZE[1] - 2 * OBSTACLE_HEIGHT,
        w * OBSTACLE_WIDTH,
        2 * OBSTACLE_HEIGHT,
    )
    for w in (2, 4, 6)
] + [
    (
        ARENA_SIZE[0] - 2 * OBSTACLE_WIDTH,
        ARENA_SIZE[1] - PLAYER_HEIGHT - 3 * OBSTACLE_HEIGHT,
        w * OBSTACLE_WIDTH,
        2 * OBSTACLE_HEIGHT,
    )
    for w in (2, 4, 6)
]  # difference width obstacles
PLAYER_SPEED = -250
PLAYER_MAX_JUMP = 5
OBSTACLE_SPEED = 200
GRAVITY = 300
ACCELERATE_BAND = 1e-2
# speed up
NEXT_STAGE_SCORE = 10 * FPS
NEXT_STAGE_SPEEDUP = 0.2
# expect 2FPS 1OBSTACLE -> (e[x]-p) FPS 1OBSTACLE ->
OBSTACLE_LEAST_PERIOD = int(0.5 * FPS)
OBSTACLE_EXPECT_FPS = 2 * FPS
# poisson distribution at k=1
OBSTACLE_LAMBDA = OBSTACLE_EXPECT_FPS - OBSTACLE_LEAST_PERIOD


# State machine constants
STATE_POP = 0  # for convenience, not really a state which we can be in
STATE_MENU = 1
STATE_PLAY = 2
STATE_STOP = 3  # not implemented yet
STATE_ENDGAME = 4


# controller
PLAYER_KEYS = {
    pg.K_UP: (0, "up"),
}
