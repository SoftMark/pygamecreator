import pygame
from pygamecreator.display import Display
from pygamecreator.static.keys import *
from pygamecreator.game_loop import GameLoop, game_loop_action

x = 0
y = 0
width = 50
height = 50


@game_loop_action
def move_right():
    global x
    x += 1


@game_loop_action
def render():
    disp.win.fill((0, 0, 0))
    pygame.draw.rect(disp.win, (0, 0, 255), (x, y, width, height))


disp = Display()
game_loop = GameLoop()
game_loop.on_key_pressed(K_RIGHT, move_right())
game_loop.while_running(render())
game_loop.run()
