import pygame

from abc import ABC, abstractmethod
from bson import ObjectId

from pygamecreator.display import Display
from pygamecreator.static.game_loop import DEFAULT_DELAY_TIME, EventTypes


class GameLoop():
    def __init__(self, display=Display(), delay=DEFAULT_DELAY_TIME):
        """
        :param display: game display
        :type display: Display

        :param delay: delay in milliseconds
        :type delay: int
        """
        self.display = display
        self.delay = delay
        self._run = True
        self._events = []

    def on_key_pressed(self, key, action):
        """
        :param key: key pygame index
        :type key: int

        :param action: action that should run on key pressed
        :type action: GameLoopAction

        :return: None
        """
        self._events.append(KeyPressedEvent(key, action))

    def while_running(self, action):
        """
        :param key: key pygame index
        :type key: int

        :param action: action that should run on key pressed
        :type action: GameLoopAction

        :return: None
        """
        self._events.append(GameLoopInitializedEvent(action))

    def run(self):
        while self._run:
            pygame.time.delay(self.delay)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._run = False
            pressed_keys = pygame.key.get_pressed()
            for event in self._events:
                if isinstance(event, KeyPressedEvent) and pressed_keys[event.key]:
                    event.action.run_action()
                elif isinstance(event, GameLoopInitializedEvent):
                    event.action.run_action()
            pygame.display.update()
            self.display.fill()
        pygame.quit()


class GameLoopAction(ABC):
    @abstractmethod
    def run_action(self):
        pass


def game_loop_action(foo):
    return type(
        f"GameLoopAction{ObjectId()}",
        (GameLoopAction, ),
        {"run_action": lambda self: foo()}
    )


class GameLoopEvent():
    def __init__(self, event_type, action):
        """
        :param event_type: type of event
        :type event_type: str

        :param action: actions that run when event triggered
        :type action: GameLoopAction
        """
        self.event_type = event_type
        self.action = action


class GameLoopInitializedEvent(GameLoopEvent):
    def __init__(self, action):
        """
        :param action: actions that run when event triggered
        :type action: GameLoopAction
        """
        super().__init__(
            event_type=EventTypes.LOOP_INITIALIZED.name,
            action=action
        )


class KeyPressedEvent(GameLoopEvent):
    def __init__(self, key, action):
        """
        :param key: pygame key identity that should trigger event
        :param key: int

        :param action: actions that run when event triggered
        :type action: GameLoopAction
        """
        super().__init__(
            event_type=EventTypes.KEY_PRESSED.name,
            action=action
        )
        self.key = key
