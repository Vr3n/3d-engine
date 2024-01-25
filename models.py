from typing import Tuple
import numpy as np
import glm
import pygame as pg

class BaseModel:
	def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)) -> None:
		self.app = app
		self.pos = pos
		self.scale = scale
		self.rot = glm.vec3([glm.radians(a) for a in rot])
		self.m_model = self.get_model_matrix()
		self.tex_id = tex_id
		self.vao = app.mesh.vao.vaos[vao_name]
		self.program = self.vao.program
		self.camera = self.app.camera

	def update(self): ...

	def get_model_matrix(self):
		m_model = glm.mat4()
		m_model = glm.translate(m_model, self.pos)

		# rotate
		m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
		m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
		m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))


		#scale
		m_model = glm.scale(m_model, self.scale)

		return m_model

	def render(self):
		self.update()
		self.vao.render()

class ExtendedBaseModel(BaseModel):
	def __init__(self, app, vao_name: str, tex_id: str | int, pos: Tuple[int, int, int], rot: Tuple[int, int, int], scale: Tuple[int, int, int]) -> None:
		super().__init__(app, vao_name, tex_id, pos, rot, scale)
		self.on_init()


	def update(self):
		self.texture.use()
		self.program['m_model'].write(self.m_model)
		self.program['m_view'].write(self.app.camera.m_view)
		self.program['camPos'].write(self.app.camera.position)

	def on_init(self):

		# initialize texture
		self.texture = self.app.mesh.texture.textures[self.tex_id]
		self.program['u_texture_0'] = 0
		self.texture.use()

		# pass to shader programs.
		self.program['m_proj'].write(self.app.camera.m_proj)
		self.program['m_view'].write(self.app.camera.m_view)
		self.program['m_model'].write(self.m_model)


		# light
		self.program['light.position'].write(self.app.light.position)
		self.program['light.Ia'].write(self.app.light.Ia)
		self.program['light.Id'].write(self.app.light.Id)
		self.program['light.Is'].write(self.app.light.Is)



class Cube(ExtendedBaseModel):
	"""
	Displaying Cube
	"""
	def __init__(self, app, vao_name="cube", tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)) -> None:
		super().__init__(app, vao_name, tex_id, pos, rot, scale)


class Ironman(ExtendedBaseModel):
	"""
	Displaying Cube
	"""

	def __init__(self, app, vao_name="ironman", tex_id='ironman', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)) -> None:
		super().__init__(app, vao_name, tex_id, pos, rot, scale)

class Skybox(BaseModel):

    def __init__(self, app, vao_name='skybox', tex_id='skybox',

                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):

        super().__init__(app, vao_name, tex_id, pos, rot, scale)

        self.on_init()



    def update(self):

        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))



    def on_init(self):

        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)

        # mvp

        self.program['m_proj'].write(self.camera.m_proj)

        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))


class AdvancedSkybox(BaseModel):
	def __init__(self, app, vao_name='advanced_skybox', tex_id='skybox',
				 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):

		super().__init__(app, vao_name, tex_id, pos, rot, scale)

		self.on_init()



	def update(self):
		m_view = glm.mat4(glm.mat3(self.camera.m_view))
		self.program['m_invProjView'].write(glm.inverse(self.camera.m_proj * m_view))

	def on_init(self):

	    # texture
		self.texture = self.app.mesh.texture.textures[self.tex_id]
		self.program['u_texture_skybox'] = 0
		self.texture.use(location=0)
