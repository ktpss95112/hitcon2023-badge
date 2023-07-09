import math

import pygame as pg

# view
WINDOW_CAPTION = "Challenge 2020 Homework"
WINDOW_SIZE = (800, 800)
ARENA_SIZE = (800, 800)
BACKGROUND_COLOR = pg.Color("black")
PLAYER_COLOR = pg.Color("green")
OBSTACLE_COLOR = pg.Color("magenta")
PLAYER_RADIUS = 10
OBSTACLE_RADIUS = 10

# model
FPS = 60  # frame per second
GAME_LENGTH = 30 * FPS
PLAYER_INIT_POSITION = [pg.Vector2(200, ARENA_SIZE[1] - PLAYER_RADIUS)]
OBSTACLE_INIT_POSITION = pg.Vector2(
    ARENA_SIZE[0] - OBSTACLE_RADIUS, ARENA_SIZE[1] - OBSTACLE_RADIUS
)
PLAYER_SPEED = 200
OBSTACLE_SPEED = 200
GRAVITY = -400
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
