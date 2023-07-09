import copy

import pygame as pg
from pygame.math import Vector2

import Const


class _GameObject:
    def __init__(self, left, top, width, height) -> None:
        self.__rect = pg.Rect(left, top, width, height)
        self.__position = Vector2(self.__rect.topleft)
        self.speed = Vector2(0, 0)
        self.gravity = 0

    def clip_position(self):
        self.x = max(0, min(Const.ARENA_SIZE[0] - self.rect.width, self.x))
        self.y = max(
            -Const.PLAYER_HEIGHT, min(Const.ARENA_SIZE[1] - self.height, self.y)
        )

    def clip_speed(self):
        pass

    def basic_tick(self, speedup):
        self.speed.y += self.gravity / Const.FPS * speedup
        self.position += self.speed / Const.FPS * speedup

        self.clip_position()
        self.clip_speed()

    def tick(self, speedup=1):
        self.basic_tick(speedup)

    @property
    def left(self):
        return self.__rect.left

    @property
    def right(self):
        return self.__rect.right

    @property
    def top(self):
        return self.__rect.top

    @property
    def bottom(self):
        return self.__rect.bottom

    @property
    def center(self):
        return Vector2(self.__rect.center)

    @center.setter
    def center(self, value):
        self.__rect.center = value
        self.__position = Vector2(self.__rect.topleft)

    @property
    def position(self):
        return copy.deepcopy(self.__position)

    @position.setter
    def position(self, value):
        self.__position = value
        self.__rect.topleft = self.__position

    @property
    def x(self):
        return self.__position.x

    @x.setter
    def x(self, value):
        self.__position.x = value
        self.__rect.topleft = self.__position

    @property
    def y(self):
        return self.__position.y

    @y.setter
    def y(self, value):
        self.__position.y = value
        self.__rect.topleft = self.__position

    @property
    def width(self):
        return self.__rect.width

    @property
    def height(self):
        return self.__rect.height

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, value):
        self.__rect = value
        self.__position = Vector2(self.__rect.topleft)


class Player(_GameObject):
    def __init__(self, player_id, rect=Const.PLAYER_INIT_RECT):
        super().__init__(*rect)
        self.player_id = player_id
        self.gravity = Const.GRAVITY
        self.status = "move"
        self.render_tick = 0

    def jump(self):
        if self.y >= Const.ARENA_SIZE[1] - self.height - Const.ACCELERATE_BAND:
            self.speed.y += Const.PLAYER_SPEED
            self.status = "jump"

    def clip_speed(self):
        if self.position.y == Const.ARENA_SIZE[1] - self.height:
            self.speed.y = 0
            if "jump" == self.status:
                self.status = "move"
                self.render_tick = 0

    def basic_tick(self, speedup):
        super().basic_tick(speedup)
        self.render_tick += 1


class Obstacle(_GameObject):
    def __init__(self, rect) -> None:
        super().__init__(*rect)
        self.speed.x = -Const.OBSTACLE_SPEED

    def clip_position(self):
        pass
