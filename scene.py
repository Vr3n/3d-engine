from models import *

class Scene:
	def __init__(self, app) -> None:
		self.app = app
		self.objects = []
		self.load()

	def add_object(self, obj):
		self.objects.append(obj)
		
	def load(self):
		app = self.app
		add = self.add_object

		# n, s = 80, 2
		# for x in range(-n, n, s):
		# 	for z in range(-n, n, s):
		# 		add(Cube(app, pos=(x, -s, z)))

		add(Ironman(app, pos=(0, 0, 4)))


	def render(self):
		for obj in self.objects:
			obj.render()