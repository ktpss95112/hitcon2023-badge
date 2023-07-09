import Const
from View.utils import *


class GameObject:
    def __init__(self, model) -> None:
        self.model = model
        self.initialize()

    def initialize(self):
        pass


class View_Player(GameObject):
    def __init__(self, model) -> None:
        super().__init__(model)

    def initialize(self):
        self.standing_frames = tuple(
            load_image(img).convert_alpha() for img in Const.PLAYER_STAND_IMGS
        )
        self.standing_frames = tuple(
            resize_surface(frame, Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT)
            for frame in self.standing_frames
        )

        self.jump_frames = tuple(
            load_image(img).convert_alpha() for img in Const.PLAYER_JUMP_IMGS
        )
        self.jump_frames = tuple(
            resize_surface(frame, Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT)
            for frame in self.jump_frames
        )

    def draw(self, screen):
        for player in self.model.players:
            # TODO: jump frame
            screen.blit(
                self.standing_frames[0],
                self.standing_frames[0].get_rect(center=player.center),
            )


class View_Obstacle(GameObject):
    def __init__(self, model) -> None:
        super().__init__(model)

    def draw(self, screen):
        for obstacle in self.model.obstacles:
            pg.draw.rect(screen, Const.OBSTACLE_COLOR, obstacle.rect)
