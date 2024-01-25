class ShaderProgram:
	def __init__(self, ctx):
		self.ctx = ctx
		self.programs = {}
		self.programs['default'] = self.get_program('default')
		self.programs['skybox'] = self.get_program('skybox')

	def get_program(self, shader_name: str):
		with open(f'shaders/{shader_name}.vert') as file:
			vertex_shader = file.read()

		with open(f'shaders/{shader_name}.frag') as file:
			frag_shader = file.read()

		prog = self.ctx.program(
				vertex_shader=vertex_shader,
				fragment_shader=frag_shader
			)

		return prog

	def destroy(self):
		[program.release() for program in self.programs.values()]