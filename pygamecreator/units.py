from __future__ import unicode_literals, absolute_import, division, print_function


class BaseUnit:
    def __init__(self, x=0, y=0):
        """
        :param x: unit horizontal position in pixels
        :type x: int

        :param y: unit vertical position in pixels
        :type y: int
        """
        self._x = x
        self._y = y


class RenderAbleUnit(BaseUnit):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)

    def render(self):
        self.area.render()


class MoveAbleUnit(RenderAbleUnit):
    def __init__(self, x=0, y=0, step=10):
        """
        :param step: how many pixels unit should move by one step
        :type step: int
        """
        super().__init__(x, y)
        self._step = step

    def _move_x(self, step):
        self._x += step or self._step

    def _move_y(self, step):
        self._y += step or self._step

    def move_right(self, step=None):
        self._move_x(step)

    def move_left(self, step=None):
        self._move_x(-step)

    def move_up(self, step=None):
        self._move_y(-step)

    def move_down(self, step=None):
        self._move_y(step)
