from pygamecreator.display import Display
from pygamecreator.game_loop import GameLoop
from pygamecreator.static.colors import WHITE

from pygamecreator.tests.agile_simulator.scene import SCENE

GAME_LOOP = GameLoop(
    display=Display(background_color=WHITE),
    scenes=[SCENE]
)

if __name__ == "__main__":
    GAME_LOOP.run()
