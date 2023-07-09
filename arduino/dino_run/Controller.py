import asyncio
from sys import exit
import serial as pyserial
import atexit
import pygame as pg
from time import time

import Const
from Card_control import game_control
from EventManager import *
from Model.Model import GameEngine

class CardReader:
    def __init__(self) -> None:
        self.port = "/dev/ttyUSB0"
        self.serial = pyserial.Serial(self.port)
        atexit.register(self.serial.close)
    
    async def _get_tap(self):
        return len(self.serial.read_all().strip()) > 0
    
    async def get_tap(self, func, timeout=1/Const.FPS/4):
        start_time = time()
        if timeout == -1:
            tap = await self._get_tap()
        else:
            tap = await asyncio.wait_for(self._get_tap(), timeout=timeout)
        # game
        if tap:
            func()
        end_time = time()
        if timeout != -1 and timeout > (end_time - start_time):
            await asyncio.sleep(timeout - (end_time - start_time))

class Controller:
    """
    Handles the control input. Either from keyboard or from AI.
    """

    def __init__(self, ev_manager: EventManager, model: GameEngine):
        """
        This function is called when the Controller is created.
        For more specific objects related to a game instance
            , they should be initialized in Controller.initialize()
        """
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.model = model
        self.reader = CardReader()

    def initialize(self):
        """
        This method is called when a new game is instantiated.
        """

    def notify(self, event: BaseEvent):
        """
        Called by EventManager when a event occurs.
        """
        if isinstance(event, EventInitialize):
            self.initialize()

        elif isinstance(event, EventEveryTick):
            key_down_events = []
            # Called once per game tick. We check our keyboard presses here.
            for event_pg in pg.event.get():
                # handle window manager closing our window
                if event_pg.type == pg.QUIT:
                    self.ev_manager.post(EventQuit())
                if event_pg.type == pg.KEYDOWN:
                    key_down_events.append(event_pg)

            cur_state = self.model.state_machine.peek()
            if cur_state == Const.STATE_MENU:
                self.ctrl_menu(key_down_events)
            elif cur_state == Const.STATE_PLAY:
                self.ctrl_play(key_down_events)
            elif cur_state == Const.STATE_STOP:
                self.ctrl_stop(key_down_events)
            elif cur_state == Const.STATE_ENDGAME:
                self.ctrl_endgame(key_down_events)

    def ctrl_menu(self, key_down_events):
        asyncio.run(self.reader.get_tap(lambda: self.ev_manager.post(EventStateChange(Const.STATE_PLAY)), -1))

    def ctrl_play(self, key_down_events):
        asyncio.run(self.reader.get_tap(lambda: self.ev_manager.post(EventPlayerJump())))

    def ctrl_stop(self, key_down_events):
        pass

    def ctrl_endgame(self, key_down_events):
        # TODO: Do not exit game when game ends. Restart the game instead.
        def restart(ev_manager):
            ev_manager.post(EventStateChange(Const.STATE_MENU))
            ev_manager.post(EventRestart())

        asyncio.run(self.reader.get_tap(lambda: restart(self.ev_manager), -1))