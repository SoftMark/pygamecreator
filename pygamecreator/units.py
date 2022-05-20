from __future__ import unicode_literals, absolute_import, division, print_function


class BaseUnit:
    pass


# TODO: Make move able unit
class RenderAbleUnit(BaseUnit):
    def __init__(self, step=10, x=0, y=0):
        """
        :param step: how many pixels unit should move by one step
        :type step: int

        :param x: unit horizontal position in pixels
        :type x: int

        :param y: unit vertical position in pixels
        :type y: int
        """
        self._step = step
        self._x = x
        self._y = y

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
