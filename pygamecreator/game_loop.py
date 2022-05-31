import pygame
from logging import getLogger

from pygamecreator.settings import FPS, DEFAULT_DELAY_TIME
from pygamecreator.display import Display

log = getLogger("[GameLoop]")


class GameLoop:
    def __init__(self, scenes, display=Display(), delay=DEFAULT_DELAY_TIME):
        """
        :param scenes: game scenes list
        :type scenes: list[pygamecreator.units.scene.Scene]

        :param display: game display object
        :type display: Display

        :param delay: delay in milliseconds
        :type delay: int
        """
        self.display = display
        self.delay = delay
        self._run = True
        self._clock = pygame.time.Clock()
        self._scenes = {scene.id: scene for scene in scenes}
        self._current_scene = scenes[0]

    def set_scene(self, scene_id):
        """
        :param scene_id: scene to set as current
        :type scene_id: bson.ObjectId
        """
        if scene := self._scenes.get(scene_id):
            self._current_scene = scene
        else:
            log.error(f"Not found Scene '{scene_id}'")

    def run(self):
        while self._run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
            pygame.time.delay(self.delay)
            self._current_scene.process_events()
            self._current_scene.render(self.display)
            pygame.display.update()
            self.display.fill()
            self._clock.tick(FPS)
        pygame.quit()

    def stop(self):
        self._run = False
