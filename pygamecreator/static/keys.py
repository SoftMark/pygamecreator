import pygame
from enum import Enum


class KeyType(Enum):
    MOUSE = 'mouse'
    KEYBOARD = 'keyboard'


class Key:
    def __init__(self, index: int, key_type: KeyType):
        self.index = index
        self.key_type = key_type


class KeyboardKey(Key):
    def __init__(self, index: int):
        super().__init__(index, key_type=KeyType.KEYBOARD)


K_LEFT = KeyboardKey(pygame.K_LEFT)
K_RIGHT = KeyboardKey(pygame.K_RIGHT)
K_UP = KeyboardKey(pygame.K_UP)
K_DOWN = KeyboardKey(pygame.K_DOWN)

K_A = KeyboardKey(pygame.K_a)
K_C = KeyboardKey(pygame.K_c)
K_D = KeyboardKey(pygame.K_d)


class MouseKey(Key):
    def __init__(self, index: int):
        super().__init__(index, key_type=KeyType.MOUSE)


MOUSE_LEFT = MouseKey(0)
MOUSE_RIGHT = MouseKey(2)
