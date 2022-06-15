from enum import Enum


class EventTypes(Enum):
    KEY_TRIGGERED = "key_triggered"
    LOOP_INITIALIZED = "scene_initialized"
    UNIT_PRESSED = "unit_pressed"


class SceneEvent:
    def __init__(self, event_type, action):
        """
        :param event_type: type of event
        :type event_type: EventTypes

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
            event_type=EventTypes.LOOP_INITIALIZED,
            action=action
        )


class PressedEvent(SceneEvent):
    def __init__(self, key, action):
        super().__init__(
            event_type=EventTypes.KEY_TRIGGERED,
            action=action
        )
        self.key = key


class KeyPressedEvent(PressedEvent):
    def __init__(self, key, action):
        """
        :param key: pygame key identity that should trigger event
        :param key: pygamecreator.static.keys.Key

        :param action: actions that run when event triggered
        :type action: pygamecreator.scene.action.SceneAction
        """
        super().__init__(key=key, action=action)


class KeyUnpressedEvent(PressedEvent):
    def __init__(self, key, action):
        """
        :param key: pygame key identity that should trigger event if unpressed
        :param key: pygamecreator.static.keys.Key

        :param action: actions that run when event triggered
        :type action: pygamecreator.scene.action.SceneAction
        """
        super().__init__(key=key, action=action)


class UnitPressedEvent(KeyPressedEvent):
    def __init__(self, unit_id, key, action):
        """
        :param unit_id: id of unit that should trigger action if pressed on its area
        :type unit_id: bson.ObjectId

        :param key: pygame key identity that should trigger event if unpressed
        :type key: pygamecreator.static.keys.Key

        :param action: actions that run when event triggered
        :type action: pygamecreator.scene.action.SceneAction
        """
        super().__init__(key=key, action=action)
        self.unit_id = unit_id
