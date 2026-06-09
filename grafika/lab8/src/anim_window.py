import moderngl
from pyrr import Matrix44, Vector3

import models
from base_window import BaseWindow

class AnimWindow(BaseWindow):

    def __init__(self, **kwargs):
        super(AnimWindow, self).__init__(**kwargs)

    def load_models(self):
        # TODO: Write model loading
        pass

    def init_shaders_variables(self):
        # TODO: Write init shader variables
        pass

    def on_render(self, time: float, frame_time: float):
        self.ctx.clear(0.1, 0.2, 0.3, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        projection = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        view = Matrix44.look_at(
            (-3.0, 5.0, 15.0),
            (0.0, 1.0, 0.0),
            (0.0, 1.0, 0.0),
        )

        # TODO: Write render part
