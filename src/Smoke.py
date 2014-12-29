#(C) Akimasa 2006

import pygame
from pygame.locals import *
from util import *

class Smoke(Actor):
	def __init__(self, game, x, y):
		Actor.__init__(self, game)
		self.x, self.y = x, y
		self.animation = self.makeAnimation()
	
	def makeAnimation(self):
		areas = []
		for y in range(2):
			for x in range(8):
				areas.append((x * 64, y * 64, 64, 64))
		return Animation(self.game.images['smoke'], areas, 1, False)
	
	def update(self):
		self.animation.update()
		if self.animation.isFinished():
			self.kill()
	
	def draw(self):
		s = self.animation.getSurface().subsurface(self.animation.getArea())
		self.game.display.blit(s, (self.x - (s.get_width() / 2), self.y - (s.get_height() / 2)))
