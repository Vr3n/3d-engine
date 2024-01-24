#version 330

layout (location = 0) out vec4 fragColor;

void main() {
	vec3 color = vec3(0.08, 0.06, 1);
	fragColor = vec4(color, 1.0);
}