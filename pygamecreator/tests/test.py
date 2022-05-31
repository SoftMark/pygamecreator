from pygamecreator.static.keys import *
from pygamecreator.game_loop import GameLoop
from pygamecreator.scene.action import scene_action
from pygamecreator.scene.scene import Scene
from pygamecreator.scene.units.sprites import SpritesStorage
from pygamecreator.scene.units.units import MoveAbleUnit


SLEEP_STATE = "sleep"
WALK_STATE = "walk"

sprites_storage = SpritesStorage.from_dict(
    {
        SLEEP_STATE: ["bitmap.png"],
        WALK_STATE: ["legs.png", "l_leg_up.png", "legs.png", "r_leg_up.png"]
    }
)

PLAYER = MoveAbleUnit(x=0, y=0, sprites_storage=sprites_storage, animation_frequency=0.1, step=10)


@scene_action
def move_right():
    PLAYER.set_sprites_state(WALK_STATE)
    PLAYER.move_right()


@scene_action
def move_left():
    PLAYER.set_sprites_state(WALK_STATE)
    PLAYER.move_left()


@scene_action
def sleep():
    PLAYER.set_sprites_state(SLEEP_STATE)


SCENE = Scene(units=[PLAYER])

SCENE.on_key_pressed(K_RIGHT, move_right())
SCENE.on_key_pressed(K_LEFT, move_left())
SCENE.on_keys_unpressed((K_RIGHT, K_LEFT), sleep())

GAME_LOOP = GameLoop(scenes=[SCENE])
GAME_LOOP.run()
