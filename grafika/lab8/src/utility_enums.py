from collections import namedtuple
from enum import Enum

Colour = namedtuple('Colour', ['name', 'rgb_value'])


class ColourRGB(Enum):
    @property
    def colour_name(self):
        return self.value.name

    @property
    def colour_rgb_value(self):
        return self.value.rgb_value

    RED = Colour("red", (1.0, 0.0, 0.0))
    ORANGE = Colour("orange", (1.0, 0.5, 0.0))
    YELLOW = Colour("yellow", (1.0, 1.0, 0.0))
    GREEN = Colour("green", (0.0, 0.8, 0.2))
    CYAN = Colour("cyan", (0.0, 0.8, 1.0))
    BLUE = Colour("blue", (0.0, 0.2, 1.0))
    PURPLE = Colour("purple", (0.6, 0.0, 1.0))
    PINK = Colour("pink", (1.0, 0.0, 0.6))

    @classmethod
    def get_by_index(cls, student_index: int):
        colour_id = student_index % 8
        return list(cls)[colour_id]
