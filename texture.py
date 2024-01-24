import pygame as pg
import moderngl as mgl


class Texture:
	def __init__(self, ctx) -> None:
		self.ctx = ctx
		self.textures = {}
		self.textures[0] = self.get_texture(path="textures/drive.jpg")


	def get_texture(self, path:str):
		texture = pg.image.load(path).convert()
		texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
		texture = self.ctx.texture(size=texture.get_size(), components=3,
								    data=pg.image.tostring(texture, 'RGB'))
		return texture

	def destory(self):
		[tex.release() for tex in self.textures.values()]