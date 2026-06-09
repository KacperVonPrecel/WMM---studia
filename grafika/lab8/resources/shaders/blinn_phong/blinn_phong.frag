#version 330

out vec4 f_color;

void main()
{
	vec3 ambient = light_ambient * material_ambient;
	vec3 diffuse = vec3(0, 0, 0);
	vec3 specular = vec3(0, 0, 0);

	vec3 phong_color = clamp(ambient + diffuse + specular, 0.0, 1.0);
	
	f_color = vec4(phong_color, 1.0);
}
