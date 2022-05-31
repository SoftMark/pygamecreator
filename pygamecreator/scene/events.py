from enum import Enum


class EventTypes(Enum):
    KEY_PRESSED = "key_pressed"
    LOOP_INITIALIZED = "scene_initialized"


class SceneEvent:
    def __init__(self, event_type, action):
        """
        :param event_type: type of event
        :type event_type: str

        :param action: actions that run when event triggered
        :type action: pygamecreator.scene.action.SceneAction
        """
        self.event_type = event_type
        self.action = action


class SceneInitializedEvent(SceneEvent):
    def __init__(self, action):
        """
        :param action: actions that run when event triggered
        :type action: pygamecreator.scene.action.SceneAction
        """
        super().__init__(
            event_type=EventTypes.LOOP_INITIALIZED.name,
            action=action
        )


class KeyPressedEvent(SceneEvent):
    def __init__(self, key, action):
        """
        :param key: pygame key identity that should trigger event
        :param key: int

        :param action: actions that run when event triggered
        :type action: pygamecreator.scene.action.SceneAction
        """
        super().__init__(
            event_type=EventTypes.KEY_PRESSED.name,
            action=action
        )
        self.key = key


class KeyUnpressedEvent(SceneEvent):
    def __init__(self, key, action):
        """
        :param key: pygame key identity that should trigger event if unpressed
        :param key: int

        :param action: actions that run when event triggered
        :type action: pygamecreator.scene.action.SceneAction
        """
        super().__init__(
            event_type=EventTypes.KEY_PRESSED.name,
            action=action
        )
        self.key = key
