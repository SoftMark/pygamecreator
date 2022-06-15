from bson import ObjectId

from pygamecreator.settings import FPS


class BaseUnit:
    def __init__(self, x=0, y=0):
        """
        :param x: unit horizontal position in pixels
        :type x: int

        :param y: unit vertical position in pixels
        :type y: int

        """
        self.id = ObjectId()
        self._x = x
        self._y = y

    @property
    def position(self):
        return self._x, self._y

    def set_position(self, position):
        self._x = position[0]
        self._y = position[1]


class RenderAbleUnit(BaseUnit):
    def __init__(self, x, y, sprites_storage, animation_frequency=0.1):
        """
        :param sprites_storage: unit sprites
        :type sprites_storage: pygamecreator.scene.units.sprites.SpritesStorage

        :param animation_frequency: how often unit should change sprite in seconds
        :type animation_frequency: float
        """
        super().__init__(x, y)
        self._sprites_storage = sprites_storage
        self.current_sprite = self._current_sprites.current_sprite
        self._animate_enabled = True
        self._animation_frequency = animation_frequency
        self._animation_counter = 0

    @property
    def _current_sprites(self):
        return self._sprites_storage.current_sprites

    def _sprite_shift(self):
        self._current_sprites.shift()
        self.current_sprite = self._current_sprites.current_sprite

    def set_sprites_state(self, state_name):
        self._sprites_storage.set_sprites_by_state(state_name)

    def _process_animation(self):
        time_spent = self._animation_counter / FPS
        if time_spent < self._animation_frequency:
            self._animation_counter += 1
        else:
            self._sprite_shift()
            self._animation_counter = 0

    def _on_pre_render(self):
        pass

    def render(self, display):
        """
        :param display: to display area
        :type display: pygamecreator.display.Display
        """
        self._on_pre_render()
        if self._animate_enabled:
            self._process_animation()
        display.win.blit(self.current_sprite.surface, (self._x, self._y))


class MoveAbleUnit(RenderAbleUnit):
    def __init__(self, x, y, sprites_storage, animation_frequency, step):
        """
        :param step: how many pixels unit should move by one step
        :type step: int
        """
        super().__init__(x, y, sprites_storage, animation_frequency)
        self._step = step

    def _move_x(self, step):
        self._x += step

    def _move_y(self, step):
        self._y += step

    def move_right(self, step=None):
        self._move_x(step or self._step)

    def move_left(self, step=None):
        self._move_x(-(step or self._step))

    def move_up(self, step=None):
        self._move_y(-(step or self._step))

    def move_down(self, step=None):
        self._move_y(step or self._step)
