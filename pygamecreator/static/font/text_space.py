import pygame
from enum import Enum

from pygamecreator.static.colors import BLACK

class FontName(Enum):
    FREESANSBOLD = "freesansbold"


def generate_text_space(text, font_name=FontName.FREESANSBOLD.value, font_size=15, color=BLACK):
    text_space = pygame.font.Font(f'{font_name}.ttf', font_size)
    return text_space.render(text, True, color)
