#version 330

layout (location = 1) in vec3 in_normal;
layout (location = 0) in vec2 in_texcoord_0;
layout (location = 2) in vec3 in_position;

uniform mat4 m_proj;
uniform mat4 m_view_light;
uniform mat4 m_model;

vec2 uv_0;

void main () {
	uv_0 = in_texcoord_0;
	mat4 mvp = m_proj * m_view_light * m_model;
	gl_Position = mvp * vec4(in_position, 1.0);
}