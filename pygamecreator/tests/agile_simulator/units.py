import pygame
import random

from enum import Enum
from logging import getLogger

from pygamecreator.static.colors import BLACK
from pygamecreator.static.font.text_space import generate_text_space
from pygamecreator.tools.surface import create_surface

from pygamecreator.scene.units.sprites import SpritesStorage, Sprite
from pygamecreator.scene.units.units import MoveAbleUnit, BaseUnit


log = getLogger("[AGILE_UNITS]")


class TaskType(Enum):
    BUG = "bug"
    FEATURE = "feature"


class TasksDifficultlyLevel(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class TaskStatus(Enum):
    TO_DO = "to do"
    IN_PROGRESS = "in progress"
    DONE = "done"


class Task(BaseUnit):
    def __init__(self, creator_id, assignee_id, assignee_sprite,
                 dashboard_id, task_status, task_type, difficulty_level):
        super().__init__()
        self.creator_id = creator_id
        self.assignee_id = assignee_id
        self.assignee_sprite = assignee_sprite
        self.dashboard_id = dashboard_id
        self.task_status = task_status
        self.task_type = task_type
        self.task_name = ("BUG_" if self.task_type == TaskType.BUG else "FEATURE_") + f"{random.randint(1, 1000)}"
        self.difficulty_level = difficulty_level
        self.code_rows = random.randint(100, 1000) if self.task_type == TaskType.FEATURE else random.randint(1, 20)
        self._k = random.randint(1, 3) if self.task_type == TaskType.FEATURE else random.randint(1, 10)
        self.total_points = self.code_rows * self.points_for_code_row
        self.progress_points = 0
        self.border = False

    def border_on(self):
        self.border = True

    def border_off(self):
        self.border = False

    @property
    def done(self) -> bool:
        return self.progress_points >= self.total_points

    @property
    def points_for_code_row(self):
        if self.difficulty_level == TasksDifficultlyLevel.EASY:
            return random.randint(1, 3) * self._k
        elif self.difficulty_level == TasksDifficultlyLevel.MEDIUM:
            return random.randint(4, 6) * self._k
        elif self.difficulty_level == TasksDifficultlyLevel.HARD:
            return random.randint(7, 10) * self._k
        else:
            NotImplementedError()

    @property
    def task_type_sprite(self):
        if self.task_type == TaskType.FEATURE:
            return Sprite('task_feature.png')
        elif self.task_type == TaskType.BUG:
            return Sprite('task_bug.png')
        else:
            NotImplementedError()

    @property
    def sprite_small(self):
        if self.difficulty_level == TasksDifficultlyLevel.EASY:
            background_path = 'task_easy_small.png'
        elif self.difficulty_level == TasksDifficultlyLevel.MEDIUM:
            background_path = 'task_medium_small.png'
        else:  # self.difficulty_level == TasksDifficultlyLevel.HARD:
            background_path = 'task_hard_small.png'

        sprite = Sprite(background_path)
        surface = sprite.surface
        text_space = generate_text_space(self.task_name, font_size=10)
        text_x = (surface.get_width() - text_space.get_width()) // 2
        text_y = (surface.get_height() - text_space.get_height()) // 2
        surface.blit(text_space, (text_x, text_y))
        sprite.surface = surface
        return sprite

    @property
    def sprite(self):
        if self.difficulty_level == TasksDifficultlyLevel.EASY:
            background_path = 'task_easy.png'
        elif self.difficulty_level == TasksDifficultlyLevel.MEDIUM:
            background_path = 'task_medium.png'
        else:  # self.difficulty_level == TasksDifficultlyLevel.HARD:
            background_path = 'task_hard.png'

        sprite = Sprite(background_path)
        surface = sprite.surface

        task_type_surface = self.task_type_sprite.surface
        task_type_x = 5
        task_type_y = (surface.get_height() - task_type_surface.get_height()) // 2
        surface.blit(task_type_surface, (task_type_x, task_type_y))

        text_space = generate_text_space(self.task_name)
        text_x = task_type_x + task_type_surface.get_width() + 5
        text_y = task_type_y + (task_type_surface.get_height() - text_space.get_height()) // 2
        surface.blit(text_space, (text_x, text_y))

        if self.assignee_sprite:
            assignee_surface = self.assignee_sprite.surface
            assignee_x = surface.get_width() - assignee_surface.get_width() - 5
            assignee_y = 5
            surface.blit(assignee_surface, (assignee_x, assignee_y))

        if self.border:
            pygame.draw.rect(surface, BLACK, (0, 0, surface.get_width(), surface.get_height()), 2)

        return sprite


class DashboardLabel(BaseUnit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Sprite("dashboard_label.png")

    def render(self, display):
        """
        :param display: to display area
        :type display: pygamecreator.display.Display
        """
        display.win.blit(self.sprite.surface, (self._x, self._y))


class Dashboard(BaseUnit):
    def __init__(self, name, x=0, y=0):
        super().__init__(x, y)
        self.name = name
        self.tasks_map = {}

        self.to_do_sprite = Sprite("dashboard_column_todo.png")
        self.in_progress_sprite = Sprite("dashboard_column_in_progress.png")
        self.done_sprite = Sprite("dashboard_column_done.png")

    @property
    def tasks_map_by_status(self):
        tasks_map_by_status = {
            TaskStatus.TO_DO: [],
            TaskStatus.IN_PROGRESS: [],
            TaskStatus.DONE: []
        }
        for task in self.tasks_map.values():
            tasks_map_by_status[task.task_status].append(task)
        return tasks_map_by_status

    def add_task(self, task):
        self.tasks_map[task.id] = task

    def change_task_status(self, task_id, status):
        task = self.pop_task(task_id)
        task.task_status = status
        self.add_task(task)

    def get_task_by_id(self, task_id):
        if task := self.tasks_map.get(task_id):
            return task
        log.error(f"Task {task_id} not found for dashboard {self.id}")

    def pop_task_for_assignee(self, assigner_id):
        """
        :rtype: Task | None
        """
        for task in self.tasks_map.values():
            if task.assignee_id == assigner_id and task.task_status == TaskStatus.TO_DO:
                return self.tasks_map.pop(task.id)
        log.info(f"Not found task for assigner {assigner_id}")
        return None

    def pop_task(self, task_id):
        """
        :rtype: Task
        """
        return self.tasks_map.pop(task_id)

    def remove_task(self, task_id):
        self.tasks_map.pop(task_id)

    def assign_task(self, task_id, assignee_id, assignee_sprite):
        if self.tasks_map[task_id].task_status == TaskStatus.TO_DO:
            self.tasks_map[task_id].assignee_id = assignee_id
            self.tasks_map[task_id].assignee_sprite = assignee_sprite

    def _enrich_with_tasks(self, column_surface, column_position, tasks):
        y = 47  # Space for column name
        for i, task in enumerate(tasks[:8]):
            x = (column_surface.get_width() - task.sprite.surface.get_width()) // 2
            column_surface.blit(task.sprite.surface, (x, y))
            x_absolute = self._x + column_position[0] + x
            y_absolute = self._y + column_position[1] + y
            task.set_position((x_absolute, y_absolute))
            y += 5 + task.sprite.surface.get_height()
        return column_surface

    @property
    def _task_status_to_column_sprite(self):
        return {
            TaskStatus.TO_DO: self.to_do_sprite,
            TaskStatus.IN_PROGRESS: self.in_progress_sprite,
            TaskStatus.DONE: self.done_sprite
        }

    def _enrich_with_columns(self, dashboard_surface):
        for i, status in enumerate([TaskStatus.TO_DO, TaskStatus.IN_PROGRESS, TaskStatus.DONE]):
            column_x = self.to_do_sprite.surface.get_width() * i
            column_position = (column_x, 0)
            tasks = self.tasks_map_by_status[status]
            column_sprite = self._task_status_to_column_sprite[status]
            column_sprite.renew()
            enriched_column_surface = self._enrich_with_tasks(column_sprite.surface, column_position, tasks)
            dashboard_surface.blit(enriched_column_surface, column_position)
        return dashboard_surface

    @property
    def surface(self):
        width = 3 * self.to_do_sprite.surface.get_width()
        height = self.to_do_sprite.surface.get_height()
        surface = self._enrich_with_columns(create_surface(width, height))
        return surface

    def render(self, display):
        """
        :param display: to display area
        :type display: pygamecreator.display.Display
        """
        display.win.blit(self.surface, (self._x, self._y))


class ProjectManager(BaseUnit):
    def __init__(self):
        super().__init__()

    def create_task(self, dashboard):
        task = Task(
            creator_id=self.id,
            assignee_id=None,
            assignee_sprite=None,
            dashboard_id=dashboard.id,
            task_status=TaskStatus.TO_DO,
            task_type=random.choice([t for t in TaskType]),
            difficulty_level=random.choice([t for t in TasksDifficultlyLevel])
        )
        dashboard.add_task(task)
        return task

    def assign_task(self, dashboard, task_id, assignee):
        dashboard.assign_task(task_id, assignee.id, assignee.task_sprite)

    def remove_task(self, dashboard, task_id):
        dashboard.remove_task(task_id)


class Project:
    def __init__(self, code_rows: int):
        self.code_rows = code_rows
        self.tasks = []
        self.done_tasks = []

    def generate_tasks(self, project_manager: ProjectManager, dashboard: Dashboard):
        generate_task_rows = 0
        while generate_task_rows < self.code_rows:
            task = project_manager.create_task(dashboard)
            generate_task_rows += task.code_rows


class ProgrammerState(Enum):
    SLEEP = "sleep"
    WORK = "work"


class Programmer(MoveAbleUnit):
    def __init__(self, x, y, sprites_storage, task_sprite, rank, speed, salary):
        """
        :param rank: programmer rank
        :param speed: task points per minute
        """
        super().__init__(x, y, sprites_storage=sprites_storage, animation_frequency=0.01, step=10)
        self.task_sprite = task_sprite
        self.rank = rank
        self.speed = speed
        self.task = None
        self.salary = salary

    def _process_task(self):
        self.task.progress_points += self.speed

    def _set_sleep_state(self):
        self._sprites_storage.set_sprites_by_state(ProgrammerState.SLEEP.name)

    def _set_work_state(self):
        self._sprites_storage.set_sprites_by_state(ProgrammerState.WORK.name)

    def work(self, dash_board: Dashboard):
        if not self.task:
            self.take_task(dash_board)

        if not self.task:  # If task not found
            self._set_sleep_state()
            return

        if self.task.done:
            dash_board.change_task_status(self.task.id, TaskStatus.DONE)
            self.task = None
        else:
            self._set_work_state()
            self._process_task()

        return dash_board

    def take_task(self, dash_board: Dashboard):
        if new_task := dash_board.pop_task_for_assignee(self.id):
            new_task.task_status = TaskStatus.IN_PROGRESS
            dash_board.add_task(new_task)
            self.task = new_task

    def _on_pre_render(self):
        self.current_sprite.renew()
        if self.task:
            self.current_sprite.surface.blit(self.task.sprite_small.surface, (80, 33))


class Ranks(Enum):
    JUNE = "june"
    MIDDLE = "middle"
    SENIOR = "senior"
    LEAD = "lead"


class June(Programmer):
    SPRITE = SpritesStorage.from_dict({
        ProgrammerState.WORK.name: ["programmer_june_work.png"],
        ProgrammerState.SLEEP.name: ["programmer_june_sleep.png"]
    })

    def __init__(self, x, y):
        super().__init__(
            x, y, sprites_storage=self.SPRITE,
            task_sprite=Sprite('programmer_june_small.png'),
            rank=Ranks.JUNE, speed=random.randint(1, 5),
            salary=random.randint(3, 9)
        )


class Middle(Programmer):
    SPRITE = SpritesStorage.from_dict({
        ProgrammerState.WORK.name: ["programmer_middle_work.png"],
        ProgrammerState.SLEEP.name: ["programmer_middle_sleep.png"]
    })

    def __init__(self, x, y):
        super().__init__(
            x, y, sprites_storage=self.SPRITE,
            task_sprite=Sprite('programmer_middle_small.png'),
            rank=Ranks.MIDDLE, speed=random.randint(4, 10),
            salary = random.randint(10, 20)
        )


class Senior(Programmer):
    SPRITE = SpritesStorage.from_dict({
        ProgrammerState.WORK.name: ["programmer_senior_work.png"],
        ProgrammerState.SLEEP.name: ["programmer_senior_sleep.png"]
    })

    def __init__(self, x, y):
        super().__init__(
            x, y, sprites_storage=self.SPRITE,
            task_sprite=Sprite('programmer_senior_small.png'),
            rank=Ranks.SENIOR, speed=random.randint(8, 15),
            salary=random.randint(15, 40)
        )


class SpendingProcessor(BaseUnit):
    def __init__(self, money_per_hour=0):
        super().__init__()
        self.minutes = 0
        self.money_per_hour = money_per_hour

    def minutes_increase(self):
        self.minutes += 1

    def render(self, display):
        """
        :type display: pygamecreator.display.Display
        """
        hours = self.minutes // 60
        minutes = self.minutes % 60
        total_spent = hours * self.money_per_hour
        time_board = generate_text_space(f"TIME SPENT: {hours}h {minutes}m", font_size=20)
        display.win.blit(time_board, self.position)
        display.win.blit(generate_text_space(f"MONEY SPENT: {total_spent}$", font_size=20),
                         (self.position[0], self.position[1] + time_board.get_height()))


PROJECT_MANAGER = ProjectManager()

DASHBOARD_LABEL = DashboardLabel(x=590, y=40)
DASHBOARD = Dashboard(name="Back-End", x=400, y=125)
DASHBOARD_DETAILS = [DASHBOARD_LABEL, DASHBOARD]

LANDING_PROJECT = Project(5000)
LANDING_PROJECT.generate_tasks(PROJECT_MANAGER, DASHBOARD)

JUNE = June(x=140, y=515)
MIDDLE = Middle(x=140, y=340)
SENIOR = Senior(x=140, y=170)
PROGRAMMERS = [JUNE, MIDDLE, SENIOR]

TIME_COUNTER = SpendingProcessor(sum([p.salary for p in PROGRAMMERS]))
