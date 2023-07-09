import numpy.random
import pygame as pg

import Const
from EventManager import *


class StateMachine(object):
    """
    Manages a stack based state machine.
    peek(), pop() and push() perform as traditionally expected.
    peeking and popping an empty stack returns None.
    """

    def __init__(self):
        self.statestack = []

    def peek(self):
        if len(self.statestack) > 0:
            return self.statestack[-1]
        return None

    def pop(self):
        if len(self.statestack) > 0:
            return self.statestack.pop()
        return None

    def push(self, state):
        self.statestack.append(state)
        return state

    def clear(self):
        self.statestack = []


class GameEngine:
    """
    The main game engine. The main loop of the game is in GameEngine.run()
    """

    def __init__(self, ev_manager: EventManager):
        """
        This function is called when the GameEngine is created.
        For more specific objects related to a game instance
            , they should be initialized in GameEngine.initialize()
        """
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.state_machine = StateMachine()

    def initialize(self):
        """
        This method is called when a new game is instantiated.
        """
        self.clock = pg.time.Clock()
        self.state_machine.push(Const.STATE_MENU)
        self.players = [Player(0)]
        self.obstacles = []
        self.next_obstacle_tick = 0
        self.score = 0
        self.speedup = 1
        self.next_stage_score = Const.NEXT_STAGE_SCORE

    def notify(self, event: BaseEvent):
        """
        Called by EventManager when a event occurs.
        """
        if isinstance(event, EventInitialize):
            self.initialize()

        elif isinstance(event, EventEveryTick):
            cur_state = self.state_machine.peek()
            if cur_state == Const.STATE_MENU:
                self.update_menu()
            elif cur_state == Const.STATE_PLAY:
                self.update_objects()
                self.update_players()

                # collide -> end
                for obstacle in self.obstacles:
                    for player in self.players:
                        dist2 = pg.math.Vector2.length_squared(
                            obstacle.position - player.position
                        )
                        if dist2 < (Const.PLAYER_RADIUS + Const.OBSTACLE_RADIUS) ** 2:
                            self.ev_manager.post(EventGameOver())

                # generate obstacle
                self.next_obstacle_tick -= 1
                if self.next_obstacle_tick <= 0:
                    self.obstacles.append(Obstacle())
                    self.next_obstacle_tick = Const.OBSTACLE_LEAST_PERIOD + int(
                        numpy.random.poisson(Const.OBSTACLE_LAMBDA)
                    )
                    self.next_obstacle_tick //= self.speedup
                # score update
                self.score += 1
                if self.score >= self.next_stage_score:
                    self.next_stage_score += Const.NEXT_STAGE_SCORE
                    self.speedup += Const.NEXT_STAGE_SPEEDUP

            elif cur_state == Const.STATE_ENDGAME:
                self.update_endgame()

        elif isinstance(event, EventStateChange):
            if event.state == Const.STATE_POP:
                if self.state_machine.pop() is None:
                    self.ev_manager.post(EventQuit())
            else:
                self.state_machine.push(event.state)

        elif isinstance(event, EventQuit):
            self.running = False

        elif isinstance(event, EventPlayerJump):
            self.players[event.player_id].jump()

        elif isinstance(event, EventGameOver):
            self.state_machine.push(Const.STATE_ENDGAME)

    def update_menu(self):
        """
        Update the objects in welcome scene.
        For example: game title, hint text
        """
        pass

    def update_objects(self):
        """
        Update the objects not controlled by user.
        For example: obstacles, items, special effects
        """
        for obstacle in self.obstacles:
            obstacle.position.x -= obstacle.speed * 1 / Const.FPS * self.speedup
        while self.obstacles and self.obstacles[0].position.x < 0:
            self.obstacles = self.obstacles[1:]

    def update_players(self):
        for player in self.players:
            player.position.y += player.speed * 1 / Const.FPS * self.speedup
            player.position.y = min(
                Const.ARENA_SIZE[1] - Const.PLAYER_RADIUS, player.position.y
            )
            player.speed -= Const.GRAVITY / Const.FPS * self.speedup
            if player.position.y == Const.ARENA_SIZE[1] - Const.PLAYER_RADIUS:
                player.speed = 0

    def update_endgame(self):
        """
        Update the objects in endgame scene.
        For example: scoreboard
        """
        pass

    def run(self):
        """
        The main loop of the game is in this function.
        This function activates the GameEngine.
        """
        self.running = True
        self.ev_manager.post(EventInitialize())
        while self.running:
            self.ev_manager.post(EventEveryTick())
            self.clock.tick(Const.FPS)


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.position = pg.Vector2(Const.PLAYER_INIT_POSITION[player_id])
        self.speed = 0

    def jump(self):
        if (
            self.position.y
            >= Const.ARENA_SIZE[1] - Const.PLAYER_RADIUS - Const.ACCELERATE_BAND
        ):
            self.speed -= Const.PLAYER_SPEED


class Obstacle:
    def __init__(self) -> None:
        self.position = pg.Vector2(Const.OBSTACLE_INIT_POSITION)
        self.speed = Const.OBSTACLE_SPEED
