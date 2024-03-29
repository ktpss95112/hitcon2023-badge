import pygame as pg

import Const
from EventManager import *
from Model.Model import GameEngine
from View.GameObject import *


class GraphicalView:
    """
    Draws the state of GameEngine onto the screen.
    """

    background = pg.Surface(Const.ARENA_SIZE)

    def __init__(self, ev_manager: EventManager, model: GameEngine):
        """
        This function is called when the GraphicalView is created.
        For more specific objects related to a game instance
            , they should be initialized in GraphicalView.initialize()
        """
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.model = model

        self.screen = pg.display.set_mode(Const.WINDOW_SIZE)
        pg.display.set_caption(Const.WINDOW_CAPTION)
        self.background.fill(Const.BACKGROUND_COLOR)
        self.players = View_Player(model)
        self.obstacles = View_Obstacle(model)

    def initialize(self):
        pass

    def notify(self, event):
        """
        Called by EventManager when a event occurs.
        """
        if isinstance(event, EventInitialize):
            self.initialize()

        elif isinstance(event, EventEveryTick):
            self.display_fps()

            cur_state = self.model.state_machine.peek()
            if cur_state == Const.STATE_MENU:
                self.render_menu()
            elif cur_state == Const.STATE_PLAY:
                self.render_play()
            elif cur_state == Const.STATE_STOP:
                self.render_stop()
            elif cur_state == Const.STATE_ENDGAME:
                self.render_endgame()

        elif isinstance(event, EventRestart):
            self.initialize()

    def display_fps(self):
        """
        Display the current fps on the window caption.
        """
        pg.display.set_caption(
            f"{Const.WINDOW_CAPTION} - FPS: {self.model.clock.get_fps():.2f}"
        )

    def render_menu(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)

        # draw text
        font = pg.font.Font(None, 36)
        text_surface = font.render("Beep Card To Start ...", 1, pg.Color("gray88"))
        text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

        pg.display.flip()

    def render_play(self):
        # draw background
        # TODO: create a background surface in initialization and render only diff parts of every tick
        self.screen.fill(Const.BACKGROUND_COLOR)

        # draw score
        font = pg.font.Font(None, 36)
        text_surface = font.render(f"Score:{self.model.score}", 1, pg.Color("gray88"))
        self.screen.blit(text_surface, text_surface.get_rect())

        # draw GameObjects
        self.players.draw(self.screen)
        self.obstacles.draw(self.screen)

        pg.display.flip()

    def render_stop(self):
        pass

    def render_endgame(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)

        # draw text
        font = pg.font.Font(None, 36)
        text_surface = font.render("Game Over", 1, pg.Color("gray88"))
        text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

        user_id = self.model.controller.reader.user_id.decode()
        text_surface = font.render(
            f"Your ID: {user_id}, Score: {self.model.score}", 1, pg.Color("gray88")
        )
        text_center = (text_center[0], text_center[1] + 40)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

        text_surface = font.render("Beep Card To Restart", 1, pg.Color("gray88"))
        text_center = (text_center[0], text_center[1] + 40)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

        pg.display.flip()
