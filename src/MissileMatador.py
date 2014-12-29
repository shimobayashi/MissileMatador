#(C) Akimasa 2006

import pygame
from pygame.locals import *
from util import *
import os
import sys
from Controller import Controller
import SceneTitle

class MisileMatador(Game):
	def __init__(self, replay = False):
		Game.__init__(self, replay)

	def start(self):
		self.display = pygame.display.set_mode((320, 240))
		self.fullscreen = False
		self.images = self.loadImages('data/image/*.png')
		self.sounds = self.loadSounds('data/sound/*.wav')
		self.controller = Controller()
		self.scene = SceneTitle.SceneTitle(self)
		self.frame_count = 0
	
	def update(self):
		self.updateDisplay()
		self.controller.update()
		self.scene.update()
		self.frame_count += 1
	
	def updateDisplay(self):
		keys = pygame.key.get_pressed()
		if keys[K_RALT] and keys[K_RETURN]:
			if self.fullscreen:
				self.display = pygame.display.set_mode((320, 240))
				self.fullscreen = False
			else:
				self.display = pygame.display.set_mode((320, 240), FULLSCREEN)
				self.fullscreen = True
	
	def draw(self):
		self.display.fill((0, 0, 0))
		self.scene.draw()
		pygame.display.update()
		if self.replay:
			pygame.image.save(self.display, "replay/%09d.tga" % (self.frame_count - 1))

if __name__ == '__main__':
	if len(sys.argv) >= 2 and sys.argv[1] == "-replay":
		mm = MisileMatador(replay = True)
	else:
		mm = MisileMatador()
	mm.run()
