from typing import List
import pygame as pg
import moderngl as mgl


class Texture:
	def __init__(self, ctx) -> None:
		self.ctx = ctx
		self.textures = {}
		self.textures[0] = self.get_texture(path="textures/drive.jpg")
		self.textures[1] = self.get_texture(path="textures/bully.jpg")
		self.textures[2] = self.get_texture(path="textures/andrew.jpg")
		self.textures['ironman'] = self.get_texture(path="objs/IronMan/Face_04.png")
		self.textures['skybox'] = self.get_texture_cube(dir_path="textures/skybox/")

	def get_texture_cube(self, dir_path: str, ext: str="jpg"):
		faces: List[str] = ["right", "left", "top", "bottom"] + ["front", "back"][::-1]

		# textures: List[pg.Surface] = [pg.image.load(dir_path + f'{face}.{ext}').convert() for face in faces]
		textures: List[pg.Surface] = []
		for face in faces:
			texture = pg.image.load(dir_path + f'{face}.{ext}').convert()
			if face in ["right", "left", "front", "back"]:
				texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
			else:
				texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
			textures.append(texture)


		size = textures[0].get_size()
		texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

		for i in range(6):
			texture_data = pg.image.tostring(textures[i], 'RGB')
			texture_cube.write(face=i, data=texture_data)

		return texture_cube

	def get_texture(self, path:str):
		texture = pg.image.load(path).convert()
		texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
		texture = self.ctx.texture(size=texture.get_size(), components=3,
								    data=pg.image.tostring(texture, 'RGB'))

		# mipmaps
		texture.filter= (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
		texture.build_mipmaps()

		# AF
		texture.ansiotropy = 32.0

		return texture

	def destory(self):
		[tex.release() for tex in self.textures.values()]