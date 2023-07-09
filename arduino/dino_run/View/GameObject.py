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
        self.moving_frames = tuple(
            load_image(img).convert_alpha() for img in Const.PLAYER_MOVE_IMGS
        )
        self.moving_frames = tuple(
            resize_surface(frame, Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT)
            for frame in self.moving_frames
        )

        self.jump_frames = tuple(
            load_image(img).convert_alpha() for img in Const.PLAYER_JUMP_IMGS
        )
        self.jump_frames = tuple(
            resize_surface(frame, Const.PLAYER_WIDTH, Const.PLAYER_HEIGHT)
            for frame in self.jump_frames
        )

        self.frames = {
            "move": self.moving_frames,
            "jump": self.jump_frames,
        }

        self.delay_of_frame = 8

    def draw(self, screen):
        for player in self.model.players:
            screen.blit(
                self.frames[player.status][
                    (player.render_tick // self.delay_of_frame)
                    % len(self.frames[player.status])
                ],
                self.frames[player.status][
                    (player.render_tick // self.delay_of_frame)
                    % len(self.frames[player.status])
                ].get_rect(center=player.center),
            )

            pg.draw.line(
                screen,
                Const.PLAYER_LINE_COLOR[player.status],
                (player.left, Const.ARENA_SIZE[1] - 2),
                (player.right, Const.ARENA_SIZE[1] - 2),
                width=2,
            )


class View_Obstacle(GameObject):
    def __init__(self, model) -> None:
        super().__init__(model)

    def draw(self, screen):
        for obstacle in self.model.obstacles:
            pg.draw.rect(screen, Const.OBSTACLE_COLOR, obstacle.rect)
