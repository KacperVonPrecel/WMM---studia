#version 330

in vec3 in_position;

uniform mat4 P;
uniform mat4 V;
uniform mat4 M;

void main()
{
    gl_Position = P * V * M * vec4(in_position, 1.0);
}