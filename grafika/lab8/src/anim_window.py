import moderngl
from pyrr import Matrix44, Vector3

import models
from base_window import BaseWindow

import numpy as np
from utility_enums import ColourRGB

STUDENT_INDEX = 337283


class AnimWindow(BaseWindow):

    def __init__(self, **kwargs):
        super(AnimWindow, self).__init__(**kwargs)

    def load_models(self):
        self.cube = models.load_cube(self.program)

        element_id = STUDENT_INDEX % 3

        if element_id == 0:
            self.accessory = models.load_pyramid(self.program)
            self.active_accessory_type = "HAT"
        elif element_id == 1:
            self.accessory = models.load_sphere(self.program)
            self.active_accessory_type = "BALL"
        elif element_id == 2:
            self.accessory = models.load_torus(self.program)
            self.active_accessory_type = "TORUS"

    def init_shaders_variables(self):
        self.uniform_loc_P = self.program["P"]
        self.uniform_loc_V = self.program["V"]
        self.uniform_loc_M = self.program["M"]
        self.uniform_loc_robot_colour = self.program["robot_colour"]

    def render_object(self, object_to_render, translation=(0.0, 0.0, 0.0), rotation=0.0, scale=(1.0, 1.0, 1.0)):
        """
        Utility method that allows for quick rendering of given object with given translation, rotation and scale.
        """
        model = Matrix44.from_translation(translation) * Matrix44.from_z_rotation(np.radians(rotation)) * Matrix44.from_scale(scale)
        self.uniform_loc_M.write(model.astype('f4'))
        object_to_render.render(moderngl.TRIANGLES)

    def render_animated_limb(self, object_to_render, time, base_angle, amplitude, speed, translation, local_translation, scale, phase=1.0):
        """
        Utility method that allows to animate circular movement of one object on one axis with customizable movement variables.
        (amplitude, speed, shoulder translation, local translation, scale, phase)
        """
        angle = (phase * amplitude * np.sin(speed * time)) + base_angle

        mat_scale = Matrix44.from_scale(scale)                                # scale (S)
        mat_local_trans = Matrix44.from_translation(local_translation)        # local_translation (T_local)
        mat_rotation = Matrix44.from_z_rotation(np.radians(angle))            # angle (R_z(angle))
        mat_shoulder_trans = Matrix44.from_translation(translation)           # shoulder_translaton (T_shoulder)

        model = mat_shoulder_trans * mat_rotation * mat_local_trans * mat_scale  # T_shoulder * R_z(angle) * T_local * S
        self.uniform_loc_M.write(model.astype('f4'))
        object_to_render.render(moderngl.TRIANGLES)

    def on_render(self, time: float, frame_time: float):
        self.ctx.clear(0.1, 0.2, 0.3, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        projection = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        view = Matrix44.look_at(
            (-3.0, 5.0, 15.0),
            (0.0, 1.0, 0.0),
            (0.0, 1.0, 0.0),
        )

        self.uniform_loc_P.write(projection.astype('f4'))
        self.uniform_loc_V.write(view.astype('f4'))

        # Head
        self.uniform_loc_robot_colour.value = ColourRGB.get_by_index(STUDENT_INDEX).colour_rgb_value
        self.render_object(self.cube, translation=(0.0, 5.0, 0.0), rotation=0.0, scale=(1.5, 1.5, 1.5))
        # Body
        self.uniform_loc_robot_colour.value = ColourRGB.get_by_index(STUDENT_INDEX + 1).colour_rgb_value
        self.render_object(self.cube, translation=(0.0, 2.0, 0.0), rotation=0.0, scale=(2.0, 4.0, 2.0))

        # Right arm
        self.uniform_loc_robot_colour.value = ColourRGB.get_by_index(STUDENT_INDEX + 3).colour_rgb_value
        self.render_animated_limb(
                    object_to_render=self.cube,
                    time=time,
                    base_angle=35.0,
                    amplitude=20.0,
                    speed=2.0,
                    translation=(-1.5, 4.0, 0.0),
                    local_translation=(0.0, -1.25, 0.0),
                    scale=(0.75, 2.5, 0.75),
                    phase=1.0
                )
        # Left arm
        self.render_animated_limb(
                    object_to_render=self.cube,
                    time=time,
                    base_angle=-35.0,
                    amplitude=20.0,
                    speed=2.0,
                    translation=(1.5, 4.0, 0.0),
                    local_translation=(0.0, -1.25, 0.0),
                    scale=(0.75, 2.5, 0.75),
                    phase=-1.0
                )

        # Right leg
        self.uniform_loc_robot_colour.value = ColourRGB.get_by_index(STUDENT_INDEX + 3).colour_rgb_value
        self.render_object(self.cube, translation=(-2.0, -2.0, 0.0), rotation=30.0, scale=(1.0, 3.0, 1.0))
        # Left leg
        self.render_object(self.cube, translation=(2.0, -2.0, 0.0), rotation=-30.0, scale=(1.0, 3.0, 1.0))

        # Accessory
        self.uniform_loc_robot_colour.value = ColourRGB.get_by_index(STUDENT_INDEX + 5).colour_rgb_value
        if self.active_accessory_type == "HAT":
            # Hat
            self.render_object(self.accessory, translation=(0.0, 6.0, 0.0), rotation=0.0, scale=(1.5, 1.5, 1.5))
        elif self.active_accessory_type == "BALL":
            # Ball in right hand
            self.render_object(self.accessory, translation=(-3.38, 4.88, 0.0), rotation=0.0, scale=(1.2, 1.2, 1.2))
        elif self.active_accessory_type == "TORUS":
            # Torus
            self.render_object(self.accessory, translation=(0.0, 1.0, 0.0), rotation=0.0, scale=(3.0, 1.5, 3.0))
