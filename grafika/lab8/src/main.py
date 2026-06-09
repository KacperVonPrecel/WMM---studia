from collections import namedtuple
from enum import Enum

import moderngl_window

from base_window import BaseWindow
from robot_window import RobotWindow
from anim_window import AnimWindow
from phong_window import PhongWindow
from blinn_phong_window import BlinnPhongWindow

Task = namedtuple('Task', ['window_args', 'window_cls'])


class TaskType(Enum):
    @property
    def window_args(self):
        return self.value.window_args

    @property
    def window_cls(self):
        return self.value.window_cls

    DEFAULT = Task(
        [
            "--shaders_dir_path=./resources/shaders/passthrough",
            "--shader_name=passthrough"
        ],
        BaseWindow
    )
    ROBOT = Task(
        [
            "--shaders_dir_path=./resources/shaders/robot",
            "--shader_name=robot"
        ],
        RobotWindow
    )
    ANIM = Task(
        [
            "--shaders_dir_path=./resources/shaders/robot",
            "--shader_name=robot"
        ],
        AnimWindow
    )
    PHONG = Task(
        [
            "--shaders_dir_path=./resources/shaders/phong",
            "--shader_name=phong"
        ],
        PhongWindow
    )
    BLINN_PHONG = Task(
        [
            "--shaders_dir_path=./resources/shaders/blinn_phong",
            "--shader_name=blinn_phong"
        ],
        BlinnPhongWindow
    )


if __name__ == '__main__':
    task = TaskType.ANIM
    moderngl_window.run_window_config(task.window_cls, args=task.window_args)
