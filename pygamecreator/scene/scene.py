import pygame

from bson import ObjectId
from logging import getLogger

from pygamecreator.static.keys import KeyType
from pygamecreator.tools.mouse import is_mouse_pos_in_area

from pygamecreator.scene.units.units import BaseUnit
from pygamecreator.scene.units.sprites import Sprite
from pygamecreator.scene.events import KeyPressedEvent, KeyUnpressedEvent, SceneInitializedEvent, UnitPressedEvent

log = getLogger("[SCENE]")


def describe_pressed_and_mem_keys(key_foo):
    def wrapper(self, key):
        """
        :type self: Scene
        :type key: pygamecreator.static.keys.Key
        """
        if key.key_type == KeyType.MOUSE:
            return key_foo(self, key, pygame.mouse.get_pressed(), self._mouse_mem)
        elif key.key_type == KeyType.KEYBOARD:
            return key_foo(self, key, pygame.key.get_pressed(), self._keys_mem)
        else:
            NotImplementedError("Unknown Key Type")
    return wrapper


class Scene:
    def __init__(self, name, units, background_path=None):
        """
        :param name: name of scene
        :type name: str

        :param units: related to scene units
        :type units: list[pygamecreator.scene.units.units.BaseUnit]

        :param background_path: path to background image
        :type background_path: str
        """
        self.id = ObjectId()
        self.name = name
        self.background = background_path and Sprite(background_path)
        self._units = {unit.id: unit for unit in units}
        self._events = []
        self._keys_mem = [0 for _ in range(323)]
        self._mouse_mem = [0 for _ in range(3)]

    @describe_pressed_and_mem_keys
    def _key_pressed(self, key, pressed_keys, mem_keys):
        return pressed_keys[key.index] and not mem_keys[key.index]

    @describe_pressed_and_mem_keys
    def _key_pushed(self, key, pressed_keys, mem_keys):
        return pressed_keys[key.index]

    @describe_pressed_and_mem_keys
    def _key_unpressed(self, key, pressed_keys, mem_keys):
        return not pressed_keys[key.index] and mem_keys[key.index]

    def process_events(self):
        pressed_keys = pygame.key.get_pressed()
        pressed_mouse = pygame.mouse.get_pressed()
        for event in self._events:
            if isinstance(event, KeyPressedEvent) and self._key_pressed(event.key):
                event.action.run_action()
            if isinstance(event, KeyUnpressedEvent) and self._key_unpressed(event.key):
                event.action.run_action()
            elif isinstance(event, SceneInitializedEvent):
                event.action.run_action()
            elif isinstance(event, UnitPressedEvent):
                if unit := self._units.get(event.unit_id):
                    if is_mouse_pos_in_area(
                            area=unit.current_sprite.surface,
                            area_pos=unit.position
                    ) and self._key_pressed(event.key):
                        event.action.run_action()
                else:
                    log.error(f"Unit {unit} not found for {self} scene!")
        self._keys_mem = pressed_keys
        self._mouse_mem = pressed_mouse

    def on_key_pressed(self, key, action):
        """
        :param key: key pygame index
        :type key: pygamecreator.static.keys.Key

        :param action: action that should run on key pressed
        :type action: pygamecreator.scene.action.SceneAction
        """
        self._events.append(KeyPressedEvent(key, action))

    def on_keys_unpressed(self, keys, action):
        """
        :param keys: key pygame index
        :type keys: Iterable[pygamecreator.static.keys.Key]

        :param action: action that should run if key not pressed
        :type action: pygamecreator.scene.action.SceneAction
        """
        for key in keys:
            self.on_key_unpressed(key, action)

    def on_key_unpressed(self, key, action):
        """
        :param key: key pygame index
        :type key: pygamecreator.static.keys.Key

        :param action: action that should run if key unpressed
        :type action: pygamecreator.scene.action.SceneAction
        """
        self._events.append(KeyUnpressedEvent(key, action))

    def while_running(self, action):
        """
        :param action: action that should while scene running
        :type action: pygamecreator.scene.action.SceneAction
        """
        self._events.append(SceneInitializedEvent(action))

    def on_unit_pressed(self, unit_id, key, action):
        """
        :param unit_id: id of unit that should trigger action if pressed on its area
        :type unit_id: ObjectId

        :param key: key that should trigger action if pressed
        :type key: pygamecreator.static.keys.Key

        :param action: action that should run if key not pressed
        :type action: pygamecreator.scene.action.SceneAction
        """
        self._events.append(UnitPressedEvent(unit_id, key, action))

    def pop_unit(self, unit_id):
        return self._units.pop(unit_id)

    def add_unit(self, unit: BaseUnit):
        self._units[unit.id] = unit

    def render(self, display):
        """
        :param display: to display area
        :type display: pygamecreator.display.Display
        """
        if background_spite := self.background:
            display.win.blit(background_spite.surface, (0, 0))

        for unit in self._units.values():
            unit.render(display)