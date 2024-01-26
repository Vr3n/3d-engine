from typing import Tuple
import pygame as pg
import sys


class Base:
	"""
	Base class of the Game engine.

	Implements the main loop,
	initializes windows of the app.
	sets opengl attributes.
	"""
	def __init__(self, screenSize: Tuple[int, int]=(600, 800)):
		# initialize all the pygame modules.
		pg.init()

		# Set flags to opengl.
		displayFlags = pg.DOUBLEBUF | pg.OPENGL

		# initialize buffers to perform antialiasing.
		pg.display.gl_set_attribute(
			pg.GL_MULTISAMPLEBUFFERS, 1
		)
		pg.display.gl_set_attribute(
			pg.GL_MULTISAMPLESAMPLES, 4
		)

		# use a core OPengGL profile for cross-playform compatibility.
		pg.display.gl_set_attribute(
			pg.GL_CONTEXT_PROFILE_MASK,
			pg.GL_CONTEXT_PROFILE_CORE
		)

		# create and display the window.
		self.screen = pg.display.set_mode(screenSize, displayFlags)

		# set the text that appears in the title bar of the window.
		pg.display.set_caption("Hello, Engine!")

		# determine if main loop is active.
		self.running = True

		# manage time-related data and operations.
		self.clock = pg.time.Clock()

	# implemented by child class.
	def initialize(self):
		...

	# implemented by child class.
	def update(self):
		...

	def run(self):
		"""
		Initialize the app and running the main loop.
		"""

		# startup.
		self.initialize()

		## main loop.
		while self.running:

			# processing the input.

			## update
			self.update()

			# render
			# display the image on screen.
			pg.display.flip()

			# limit to 60 fps (pauses if it goes above 60 fps.)
			self.clock.tick(60)

		# shutdown
		pg.quit()
		sys.exit()