from typing import Any
import numpy as np
from numpy.typing import NDArray
import pywavefront
import moderngl as mgl



class VBO:
	def __init__(self, ctx):
		self.vbos = {}
		self.vbos['cube'] = CubeVBO(ctx)
		self.vbos['ironman'] = IronManVBO(ctx)
		self.vbos['skybox'] = SkyboxVBO(ctx)
		self.vbos['advanced_skybox'] = AdvancedSkyboxVBO(ctx)

	def destroy(self):
		[vbo.destroy() for vbo in self.vbos.values()]

class BaseVBO:
	def __init__(self, ctx) -> None:
		self.ctx = ctx
		self.vbo = self.get_vbo()
		self.format: str | None = None
		self.attrib: str | None = None

	def get_vertex_data(self) -> NDArray[Any]: ...

	def get_vbo(self):
		vertex_data = self.get_vertex_data()
		vbo = self.ctx.buffer(vertex_data)
		return vbo

	def destroy(self):
		self.vbo.release()


class AdvancedSkyboxVBO(BaseVBO):
	def __init__(self, ctx) -> None:
		super().__init__(ctx)
		self.format = '3f'
		self.attribs = ['in_position']


	def get_vertex_data(self):
		# in clip space.
		z = 0.9999

		vertices = [
			(-1, -1, z), (3, 1, z), (-1, 3, z),
		]

		vertex_data = np.array(vertices, dtype='f4')

		return vertex_data
		
class SkyboxVBO(BaseVBO):
	def __init__(self, ctx) -> None:
		super().__init__(ctx)
		self.format = '3f'
		self.attribs = ['in_position']

	@staticmethod
	def get_data(vertices, indices):
		data = [vertices[ind] for triangle in indices for ind in triangle]
		return np.array(data, dtype='f4')

	def get_vertex_data(self):

		vertices = [(-1, -1, 1), ( 1, -1,  1), (1,  1,  1), (-1, 1,  1),

		            (-1, 1, -1), (-1, -1, -1), (1, -1, -1), ( 1, 1, -1)]



		indices = [(0, 2, 3), (0, 1, 2),

		           (1, 7, 2), (1, 6, 7),

		           (6, 5, 4), (4, 7, 6),

		           (3, 4, 5), (3, 5, 0),

		           (3, 7, 4), (3, 2, 7),

		           (0, 6, 1), (0, 5, 6)]

		vertex_data = self.get_data(vertices, indices)

		vertex_data = np.flip(vertex_data, 1).copy(order='C')

		return vertex_data


class CubeVBO(BaseVBO):
	def __init__(self, ctx) -> None:
		super().__init__(ctx)
		self.format = '2f 3f 3f'
		self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

	@staticmethod
	def get_data(vertices, indices):
		data = [vertices[ind] for triangle in indices for ind in triangle]
		return np.array(data, dtype='f4')

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

		normals = [
			(0, 0, 1) * 6,
			(1, 0, 0) * 6,
			(0, 0, -1) * 6,
			(-1, 0, 0) * 6,
			(0, 1, 0) * 6,
			(0, -1, 0) * 6,
		]

		normals = np.array(normals, dtype="f4").reshape(36, 3)

		vertex_data = np.hstack([normals, vertex_data])
		vertex_data = np.hstack([tex_coord_data, vertex_data])

		return vertex_data


class IronManVBO(BaseVBO):
	def __init__(self, ctx) -> None:
		super().__init__(ctx)
		self.format = '2f 3f 3f'
		self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

	def get_vertex_data(self) -> NDArray[Any]:
		objs = pywavefront.Wavefront('objs/IronMan/lego obj.obj')
		obj = objs.materials.popitem()[1]
		vertex_data = obj.vertices
		vertex_data = np.array(vertex_data, dtype='f4')
		return vertex_data