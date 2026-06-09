#version 330

in vec3 in_position;
in vec3 in_normal;

uniform mat4 P;
uniform mat4 V;
uniform mat4 M;

out vec3 v_position;
out vec3 v_normal;

void main()
{
	v_position = (M * vec4(in_position, 1.0)).xyz;
	v_normal = mat3(transpose(inverse(M))) * in_normal;
	gl_Position = P * V * M * vec4(in_position, 1.0);
}