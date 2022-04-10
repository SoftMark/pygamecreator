from enum import Enum

DEFAULT_DELAY_TIME = 1


class EventTypes(Enum):
    KEY_PRESSED = "key_pressed"
    LOOP_INITIALIZED = "loop_initialized"
