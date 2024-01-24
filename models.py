import numpy as np
import glm

class Triangle:
	"""
	Displaying triangle
	"""

	def __init__(self, app) -> None:
		self.app = app
		self.ctx = app.ctx
		self.vbo = self.get_vbo()
		self.shader_program = self.get_shader_program('default')
		self.vao = self.get_vao()


	def render(self):
		self.vao.render()

	def destroy(self):
		self.vbo.release()
		self.shader_program.release()
		self.vao.release()

	def get_vao(self):
		vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '3f', 'in_position')])
		return vao


	def get_vertex_data(self):
		"""
		Get the vertex points of the shape.

		The opengl has right handled y axis.
		"""
		vertex_data =[
			(-0.6, -0.8, 0.0),
			(0.6, -0.8, 0.0),
			(0.0, 0.8, 0.0),
		]

		vertex_data = np.array(vertex_data, dtype='f4')
		return vertex_data

	def get_vbo(self):
		"""
		Adding vertex data to vbo.

		Vertex buffer object.
		"""
		vertex_data = self.get_vertex_data()
		vbo = self.ctx.buffer(vertex_data)
		return vbo


	def get_shader_program(self, shader_name: str):
		with open(f'shaders/{shader_name}.vert') as file:
			vertex_shader = file.read()

		with open(f'shaders/{shader_name}.frag') as file:
			frag_shader = file.read()

		prog = self.ctx.program(
				vertex_shader=vertex_shader,
				fragment_shader=frag_shader
			)

		return prog

class Cube:
	"""
	Displaying Cube
	"""

	def __init__(self, app) -> None:
		self.app = app
		self.ctx = app.ctx
		self.vbo = self.get_vbo()
		self.shader_program = self.get_shader_program('default')
		self.vao = self.get_vao()
		self.m_model = self.get_model_matrix()
		self.on_init()

	def update(self):
		m_model = glm.rotate(self.m_model, self.app.time, glm.vec3(0, 1, 0))
		self.shader_program['m_model'].write(m_model)

	def on_init(self):
		self.shader_program['m_proj'].write(self.app.camera.m_proj)
		self.shader_program['m_view'].write(self.app.camera.m_view)
		self.shader_program['m_model'].write(self.m_model)


	def get_model_matrix(self):
		m_model = glm.mat4()
		return m_model


	def render(self):
		self.update()
		self.vao.render()

	def destroy(self):
		self.vbo.release()
		self.shader_program.release()
		self.vao.release()

	def get_vao(self):
		vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '2f 3f', 'in_texcoord_0', 'in_position')])
		return vao


	def get_vertex_data(self):
		"""
		Get the vertex points of the shape.

		The opengl has right handled y axis.
		"""
		vertex_data =[
			(-1, -1, 1),
			(1, -1, 1),
			(1, 1, 1,),
			(-1, 1, 1),
			(-1, 1, -1),
			(-1, -1, -1),
			(1, -1, -1),
			(1, 1, -1)
		]

		indices = [
			(0, 2, 3), (0, 1, 2),
			(1, 7, 2), (1, 6, 7),
			(6, 5, 4), (4, 7, 6),
			(3, 4, 5), (3, 5, 0),
			(3, 7, 4), (3, 2, 7),
			(0, 6, 1), (0, 5, 6),
		]
		vertex_data = self.get_data(vertex_data, indices)

		# texturing data.
		tex_coords = [
			(0, 0),
			(1, 0),
			(1, 1),
			(0, 1)
		]

		tex_cood_indices = [
			(0, 2, 3), (0, 1, 2),
			(0, 2, 3), (0, 1, 2),
			(0, 1, 2), (2, 3, 0),
			(2, 3, 0), (2, 0, 1),
			(0, 2, 3), (0, 1, 2),
			(3, 1, 2), (3, 0, 1),
		]

		tex_coord_data = self.get_data(tex_coords, tex_cood_indices)
		vertex_data = np.hstack([tex_coord_data, vertex_data])
		return vertex_data

	@staticmethod
	def get_data(vertices, indices):
		data = [vertices[ind] for triangle in indices for ind in triangle]
		return np.array(data, dtype='f4')

	def get_vbo(self):
		"""
		Adding vertex data to vbo.

		Vertex buffer object.
		"""
		vertex_data = self.get_vertex_data()
		vbo = self.ctx.buffer(vertex_data)
		return vbo


	def get_shader_program(self, shader_name: str):
		with open(f'shaders/{shader_name}.vert') as file:
			vertex_shader = file.read()

		with open(f'shaders/{shader_name}.frag') as file:
			frag_shader = file.read()

		prog = self.ctx.program(
				vertex_shader=vertex_shader,
				fragment_shader=frag_shader
			)

		return prog
