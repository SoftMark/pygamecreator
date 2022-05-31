from abc import ABC, abstractmethod
from bson import ObjectId


class SceneAction(ABC):
    @abstractmethod
    def run_action(self):
        pass


def scene_action(foo):
    return type(
        f"SceneAction{ObjectId()}",
        (SceneAction,),
        {"run_action": lambda self: foo()}
    )
