from pygamecreator.display import Display
from pygamecreator.static.keys import *
from pygamecreator.game_loop import GameLoop, game_loop_action
from pygamecreator.units import MoveAbleUnit


class Rect(MoveAbleUnit):
    width = 50
    height = 50
    color = (0, 0, 255)

    def render(self):
        pygame.draw.rect(
            game_loop.display.win, self.color,
            (self._x, self._y, self.width, self.height)
        )


@game_loop_action
def move_right():
    rect.move_right()


@game_loop_action
def render():
    rect.render()


rect = Rect()
game_loop = GameLoop()
game_loop.on_key_pressed(K_RIGHT, move_right())
game_loop.while_running(render())
game_loop.run()
