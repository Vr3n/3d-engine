#version 330

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;

void main() {
	vec3 color = vec3(uv_0, 1);
	fragColor = vec4(color, 1.0);
}