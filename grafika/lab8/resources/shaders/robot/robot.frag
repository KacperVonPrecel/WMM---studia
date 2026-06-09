#version 330

out vec4 f_color;

uniform vec3 robot_colour;

void main()
{
    f_color = vec4(robot_colour, 1.0);
}
