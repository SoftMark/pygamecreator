import pygame


def is_mouse_pos_in_area(area, area_pos):
    """
    :type area: pygame.Surface
    :type area_pos: tuple[int, int]
    :rtype: bool
    """
    pos = pygame.mouse.get_pos()
    if area_pos[0] < pos[0] < area_pos[0] + area.get_width():
        if area_pos[1] < pos[1] < area_pos[1] + area.get_height():
            return True
    return False
