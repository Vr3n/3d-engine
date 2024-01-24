import pygame as pg
import moderngl as mgl
import sys
import models
import camera

class GraphicsEngine:
	def __init__(self, win_size=(1920, 1080)) -> None:
		pg.init()

		self.WIN_SIZE = win_size

		# setting opengl attributes.
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
		pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

		# create opengl context
		pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)

		# mouse settings
		pg.event.set_grab(True)
		pg.mouse.set_visible(True)

		# detect and use existing opengl context.
		self.ctx = mgl.create_context()

		self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)

		# createt an obj to track time.
		self.clock = pg.time.Clock()
		self.time = 0
		self.delta_time = 0

		self.camera = camera.Camera(self)
		self.scene = models.Cube(self)

	def check_events(self):
		"""
		Checking Keyboard or mouse eevnts.
		"""

		for event in pg.event.get():
			if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
				self.scene.destroy()
				pg.quit()
				sys.exit()

	def render(self):
		self.ctx.clear(color=(0.08, 0.16, 0.18))
		self.scene.render()

		# swap the buffers.
		pg.display.flip()
		
	def get_time(self):
		self.time = pg.time.get_ticks() * 0.001


	def run(self):
		while True:
			self.get_time()
			self.check_events()
			self.camera.update()
			self.render()
			self.delta_time = self.clock.tick(60)

if __name__ == "__main__":
	app = GraphicsEngine()
	app.run()