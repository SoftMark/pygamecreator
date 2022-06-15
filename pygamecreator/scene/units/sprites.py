import os
import pygame
from logging import getLogger

from pygamecreator.settings import MEDIA_ROOT

log = getLogger("[SPRITES]")


class Sprite:
    def __init__(self, img_path):
        """
        :param img_path: Path to sprite image
        :type img_path: str
        """
        self.img_path = os.path.join(MEDIA_ROOT, img_path)
        self.surface = pygame.image.load(self.img_path)

    def renew(self):
        self.surface = pygame.image.load(self.img_path)


class SpritesMember(Sprite):
    def __init__(self, index, img_path):
        """
        :param index: needed to remember position of exact sprite
        :type index: int
        """
        super().__init__(img_path)
        self.index = index


class Sprites:
    def __init__(self, state_name, img_paths):
        """
        :param state_name: name of sprites states
        :type state_name: str

        :param img_paths: Path to sprite image
        :type img_paths: list[str]
        """
        self.state_name = state_name
        self._sprites = [SpritesMember(i, img_path) for i, img_path in enumerate(img_paths)]
        self.current_sprite = self._sprites[0]

    def shift(self):
        if self.current_sprite.index < len(self._sprites) - 1:
            self.current_sprite = self._sprites[self.current_sprite.index + 1]
        else:
            self.current_sprite = self._sprites[0]


class SpritesStorage:
    def __init__(self, sprites):
        """
        :param sprites: sequence of Sprites objects
        :type sprites: list[Sprites]
        """
        self._mapping = {sprite.state_name: sprite for sprite in sprites}
        self.current_sprites = sprites[0]

    def set_sprites_by_state(self, state_name):
        if sprites := self._mapping.get(state_name):
            if self.current_sprites.state_name != state_name:
                self.current_sprites = sprites
        else:
            log.error(f"Not found state '{state_name}' for SpritesStorage object. "
                      f"Use one of: {', '.join(self._mapping.keys())}")

    @classmethod
    def from_dict(cls, sprites_dict):
        """
        :param sprites_dict: dicts of sprites to generate
        :type sprites_dict: dict
        {%STATE_NAME%: list[%IMG_PATH%]}
        """
        return SpritesStorage(
            sprites=[Sprites(state, img_paths) for state, img_paths in sprites_dict.items()]
        )
