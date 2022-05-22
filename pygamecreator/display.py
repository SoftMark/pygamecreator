import pygame
from pygamecreator.static.display import DEFAULT_WIN_SIZE, DEFAULT_WIN_CAPTION
from pygamecreator.static.colors import BLACK


class Display:
    def __init__(self, win_size=DEFAULT_WIN_SIZE, win_caption=DEFAULT_WIN_CAPTION, background_color=BLACK):
        """
        :param win_size: size of window
        :type win_size: tuple[int, int]

        :param win_caption: caption of window
        :type win_caption: str
        """
        self.win_size = win_size
        self.win_caption = win_caption
        self.background_color = background_color

        pygame.init()
        self.win = pygame.display.set_mode(self.win_size)
        pygame.display.set_caption(self.win_caption)

    def fill(self):
        self.win.fill(self.background_color)
