#version 330

out vec4 f_color;

uniform vec3 light_position;
uniform vec3 light_ambient;
uniform vec3 light_diffuse;
uniform vec3 light_specular;
uniform vec3 material_ambient;
uniform vec3 material_diffuse;
uniform vec3 material_specular;
uniform float material_shininess;
uniform vec3 camera_position;

in vec3 v_position;
in vec3 v_normal;

void main()
{
	vec3 ambient = light_ambient * material_ambient;

	vec3 N = normalize(v_normal);
	vec3 L = normalize(light_position - v_position);
	float cosNL = max(dot(N, L), 0.0);
	vec3 diffuse = light_diffuse * material_diffuse * cosNL;

	vec3 V = normalize(camera_position - v_position);
	vec3 H = normalize(L + V);
	float spec_angle = max(dot(N, H), 0.0);
	float spec_factor = pow(spec_angle, material_shininess);

	vec3 specular = light_specular * material_specular * spec_factor;

	vec3 phong_color = clamp(ambient + diffuse + specular, 0.0, 1.0);
	f_color = vec4(phong_color, 1.0);
}