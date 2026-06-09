from pathlib import Path

import moderngl
from moderngl_window import WindowConfig

import models
from utils.shader_utils import get_shaders
from utils.config import GL_VERSION, WINDOW_TITLE


class BaseWindow(WindowConfig):
    gl_version = GL_VERSION
    title = WINDOW_TITLE

    def __init__(self, **kwargs):
        super(BaseWindow, self).__init__(**kwargs)

        shaders = get_shaders(self.argv.shaders_dir_path)
        self.program = self.ctx.program(vertex_shader=shaders[self.argv.shader_name].vertex_shader,
                                        fragment_shader=shaders[self.argv.shader_name].fragment_shader)

        self.init_shaders_variables()
        self.load_models()

    def load_models(self):
        self.quad_2d = models.load_quad_2D(self.program)

    def init_shaders_variables(self):
        pass

    @classmethod
    def add_arguments(cls, parser):
        parser.add_argument('--shaders_dir_path', type=str, required=True, help='Path to the directory with shaders')
        parser.add_argument('--shader_name', type=str, required=True,
                            help='Name of the shader to look for in the shader_path directory')

    def on_render(self, time: float, frame_time: float):
        self.ctx.clear(0.1, 0.2, 0.3, 0.0)
        self.quad_2d.render(moderngl.TRIANGLES)
