import random

from pygamecreator.tools.mouse import is_mouse_pos_in_area
from pygamecreator.static.keys import *
from pygamecreator.scene.action import scene_action
from pygamecreator.scene.scene import Scene

from pygamecreator.tests.agile_simulator.units import PROGRAMMERS, DASHBOARD, \
    DASHBOARD_DETAILS, PROJECT_MANAGER, TaskStatus, TIME_COUNTER

CURRENT_TASK = None
MINUTES_SPENT = 0


@scene_action
def create_task():
    PROJECT_MANAGER.create_task(DASHBOARD)


@scene_action
def assign_task_random():
    if tasks := DASHBOARD.tasks_map_by_status[TaskStatus.TO_DO]:
        tasks = tasks[:8]
        for task in tasks:
            PROJECT_MANAGER.assign_task(DASHBOARD, task.id, random.choice(PROGRAMMERS))


@scene_action
def assign_task():
    global CURRENT_TASK
    if CURRENT_TASK:
        for programmer in PROGRAMMERS:
            if is_mouse_pos_in_area(programmer.current_sprite.surface, programmer.position):
                PROJECT_MANAGER.assign_task(DASHBOARD, CURRENT_TASK.id, programmer)
                DASHBOARD.tasks_map[CURRENT_TASK.id].border_off()
                CURRENT_TASK = None
                break


@scene_action
def time_it():
    TIME_COUNTER.minutes_increase()


@scene_action
def work():
    for programmer in PROGRAMMERS:
        programmer.work(DASHBOARD)


@scene_action
def remove_from_done_random():
    if tasks := DASHBOARD.tasks_map_by_status[TaskStatus.DONE]:
        for task in tasks[:8]:
            PROJECT_MANAGER.remove_task(DASHBOARD, task.id)


@scene_action
def remove_task_from_done():
    if tasks := DASHBOARD.tasks_map_by_status[TaskStatus.DONE]:
        for task in tasks:
            if is_mouse_pos_in_area(task.sprite.surface, task.position):
                DASHBOARD.remove_task(task.id)
                break


@scene_action
def choose_task():
    global CURRENT_TASK
    if tasks := DASHBOARD.tasks_map_by_status[TaskStatus.TO_DO]:
        for task in tasks:
            if is_mouse_pos_in_area(task.sprite.surface, task.position):
                DASHBOARD.tasks_map[task.id].border_on()
                CURRENT_TASK = task
            else:
                DASHBOARD.tasks_map[task.id].border_off()


SCENE = Scene(name="Office", units=PROGRAMMERS + DASHBOARD_DETAILS + [TIME_COUNTER])
SCENE.on_key_pressed(K_C, create_task())
SCENE.on_key_pressed(K_A, assign_task_random())
SCENE.on_key_pressed(K_D, remove_from_done_random())
SCENE.on_key_pressed(MOUSE_LEFT, choose_task())
SCENE.on_key_pressed(MOUSE_LEFT, assign_task())
SCENE.on_key_pressed(MOUSE_LEFT, remove_task_from_done())
SCENE.while_running(work())
SCENE.while_running(time_it())
