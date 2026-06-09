import moderngl
from pyrr import Matrix44, Vector3

import models
from base_window import BaseWindow

import numpy as np
from utility_enums import ColourRGB

STUDENT_INDEX = 337283


class BlinnPhongWindow(BaseWindow):

    def __init__(self, **kwargs):
        super(BlinnPhongWindow, self).__init__(**kwargs)

    def load_models(self):
        self.cube = models.load_cube(self.program)

        element_id = STUDENT_INDEX % 3

        print(f"[DEBUG] Twój element_id to: {element_id}")

        if element_id == 0:
            print("[DEBUG] Ładuję Ostrosłup (Czapkę)")
            self.accessory = models.load_pyramid(self.program)
            self.active_accessory_type = "HAT"
        elif element_id == 1:
            print("[DEBUG] Ładuję Sferę (Kulkę)")
            self.accessory = models.load_sphere(self.program)
            self.active_accessory_type = "BALL"
        elif element_id == 2:
            print("[DEBUG] Ładuję Torus")
            self.accessory = models.load_torus(self.program)
            self.active_accessory_type = "TORUS"

    def init_shaders_variables(self):
        self.uniform_loc_P = self.program["P"]
        self.uniform_loc_V = self.program["V"]
        self.uniform_loc_M = self.program["M"]

        self.uniform_loc_camera_pos = self.program["camera_position"]
        self.uniform_loc_light_pos = self.program["light_position"]

        self.uniform_loc_light_ambient = self.program['light_ambient']
        self.uniform_loc_light_diffuse = self.program['light_diffuse']
        self.uniform_loc_light_specular = self.program['light_specular']

        self.uniform_loc_material_ambient = self.program['material_ambient']
        self.uniform_loc_material_diffuse = self.program['material_diffuse']
        self.uniform_loc_material_specular = self.program['material_specular']
        self.uniform_loc_material_shininess = self.program['material_shininess']

    def render_object(self, object_to_render, translation=(0.0, 0.0, 0.0), rotation=0.0, scale=(1.0, 1.0, 1.0)):
        model = Matrix44.from_translation(translation) * Matrix44.from_z_rotation(rotation * np.pi / 180) * Matrix44.from_scale(scale)
        self.uniform_loc_M.write(model.astype('f4'))
        object_to_render.render(moderngl.TRIANGLES)

    def configure_lighting(self, camera_pos, l_pos, l_ambient, l_diffuse, l_specular, m_ambient, m_diffuse, m_specular, m_shininess):
        self.uniform_loc_camera_pos.write(camera_pos)
        self.uniform_loc_light_pos.write(l_pos)

        self.uniform_loc_light_ambient.write(l_ambient)
        self.uniform_loc_light_diffuse.write(l_diffuse)
        self.uniform_loc_light_specular.write(l_specular)

        self.change_colour(m_ambient, m_diffuse)
        self.uniform_loc_material_specular.write(m_specular)
        self.uniform_loc_material_shininess.value = m_shininess

    def change_colour(self, m_ambient, m_diffuse):
        self.uniform_loc_material_ambient.value = m_ambient
        self.uniform_loc_material_diffuse.value = m_diffuse

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

        radius = 10.0
        light_x = radius * np.sin(time)
        light_y = 5.0
        light_z = radius * np.cos(time)

        dynamic_light_pos = np.array([light_x, light_y, light_z], dtype='f4')

        self.configure_lighting(
            camera_pos=np.array([-3.0, 5.0, 15.0], dtype='f4'),
            l_pos=dynamic_light_pos,
            l_ambient=np.array([0.2, 0.2, 0.2], dtype='f4'),
            l_diffuse=np.array([1.0, 1.0, 1.0], dtype='f4'),
            l_specular=np.array([1.0, 1.0, 1.0], dtype='f4'),
            m_ambient=np.array([1.0, 0.5, 0.0], dtype='f4'),
            m_diffuse=np.array([1.0, 0.5, 0.0], dtype='f4'),
            m_specular=np.array([1.0, 1.0, 1.0], dtype='f4'),
            m_shininess=50.0
        )

        # Colours
        colour_head = ColourRGB.get_by_index(STUDENT_INDEX).colour_rgb_value
        colour_body = ColourRGB.get_by_index(STUDENT_INDEX + 1).colour_rgb_value
        colour_arms = ColourRGB.get_by_index(STUDENT_INDEX + 3).colour_rgb_value
        colour_legs = ColourRGB.get_by_index(STUDENT_INDEX + 3).colour_rgb_value
        colour_accessory = ColourRGB.get_by_index(STUDENT_INDEX + 5).colour_rgb_value

        # Head
        self.change_colour(m_ambient=colour_head, m_diffuse=colour_head)
        self.render_object(self.cube, translation=(0.0, 5.0, 0.0), rotation=0.0, scale=(1.5, 1.5, 1.5))
        # Body
        self.change_colour(m_ambient=colour_body, m_diffuse=colour_body)
        self.render_object(self.cube, translation=(0.0, 2.0, 0.0), rotation=0.0, scale=(2.0, 4.0, 2.0))

        # Right arm
        self.change_colour(m_ambient=colour_arms, m_diffuse=colour_arms)
        self.render_object(self.cube, translation=(-2.5, 4.0, 0.0), rotation=-45.0, scale=(0.75, 2.5, 0.75))
        # Left arm
        self.render_object(self.cube, translation=(2.5, 4.0, 0.0), rotation=45.0, scale=(0.75, 2.5, 0.75))

        # Right leg
        self.change_colour(m_ambient=colour_legs, m_diffuse=colour_legs)
        self.render_object(self.cube, translation=(-2.0, -2.0, 0.0), rotation=30.0, scale=(1.0, 3.0, 1.0))
        # Left leg
        self.render_object(self.cube, translation=(2.0, -2.0, 0.0), rotation=-30.0, scale=(1.0, 3.0, 1.0))

        self.change_colour(m_ambient=colour_accessory, m_diffuse=colour_accessory)

        if self.active_accessory_type == "HAT":
            # Hat
            self.render_object(self.accessory, translation=(0.0, 6.0, 0.0), rotation=0.0, scale=(1.5, 1.5, 1.5))
        elif self.active_accessory_type == "BALL":
            # Ball in right hand
            self.render_object(self.accessory, translation=(-3.38, 4.88, 0.0), rotation=0.0, scale=(1.2, 1.2, 1.2))
        elif self.active_accessory_type == "TORUS":
            # Torus
            self.render_object(self.accessory, translation=(0.0, 1.0, 0.0), rotation=0.0, scale=(3.0, 1.5, 3.0))
