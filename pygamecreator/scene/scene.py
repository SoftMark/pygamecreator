import pygame

from bson import ObjectId

from pygamecreator.scene.units.units import BaseUnit
from pygamecreator.scene.units.sprites import Sprite
from pygamecreator.scene.events import KeyPressedEvent, KeyUnpressedEvent, SceneInitializedEvent


class Scene:
    def __init__(self, units, background_path=None):
        """
        :param units: related to scene units
        :type units: list[pygamecreator.units.units.BaseUnit]

        :param background_path: path to background image
        :type background_path: str
        """

        self.id = ObjectId()
        self.background = background_path and Sprite(background_path)
        self._units = {unit.id: unit for unit in units}
        self._events = []
        self._keys_mem = [0 for _ in range(323)]

    def process_events(self):
        pressed_keys = pygame.key.get_pressed()
        for event in self._events:
            if isinstance(event, KeyPressedEvent) and pressed_keys[event.key]:
                self._keys_mem[event.key] = 1
                event.action.run_action()
            if isinstance(event, KeyUnpressedEvent) and not pressed_keys[event.key] and self._keys_mem[event.key]:
                self._keys_mem[event.key] = 0
                event.action.run_action()
            elif isinstance(event, SceneInitializedEvent):
                event.action.run_action()

    def on_key_pressed(self, key, action):
        """
        :param key: key pygame index
        :type key: int

        :param action: action that should run on key pressed
        :type action: GameLoopAction
        """
        self._events.append(KeyPressedEvent(key, action))

    def on_keys_unpressed(self, keys, action):
        """
        :param keys: key pygame index
        :type keys: Iterable[int]

        :param action: action that should run if key not pressed
        :type action: GameLoopAction
        """
        for key in keys:
            self.on_key_unpressed(key, action)

    def on_key_unpressed(self, key, action):
        """
        :param key: key pygame index
        :type key: int

        :param action: action that should run if key not pressed
        :type action: GameLoopAction
        """
        self._events.append(KeyUnpressedEvent(key, action))

    def while_running(self, action):
        """
        :param key: key pygame index
        :type key: int

        :param action: action that should run on key pressed
        :type action: GameLoopAction
        """
        self._events.append(SceneInitializedEvent(action))

    def pop_unit(self, unit_id):
        return self._units.pop(unit_id)

    def render(self, display):
        """
        :param display: to display area
        :type display: pygamecreator.display.Display
        """
        if background_spite := self.background:
            display.win.blit(background_spite.surface, (0, 0))

        for unit in self._units.values():
            unit.render(display)