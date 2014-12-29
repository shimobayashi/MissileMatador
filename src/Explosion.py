#(C) Akimasa 2006

import pygame
from pygame.locals import *
from util import *

class Explosion(Actor):
	def __init__(self, game, x, y):
		Actor.__init__(self, game)
		self.x, self.y = x, y
		self.rect_hit = pygame.Rect(-16, -16, 32, 32)
		self.animation = self.makeAnimation()
		self.game.sounds['bom'].play()
	
	def makeAnimation(self):
		areas = []
		for y in range(8):
			for x in range(2):
				areas.append((x * 64, y * 64, 64, 64))
		return Animation(self.game.images['explosion'], areas, 3, False)
	
	def update(self):
		self.animation.update()
		if self.animation.isFinished():
			self.kill()
	
	def draw(self):
		s = self.animation.getSurface().subsurface(self.animation.getArea())
		self.game.display.blit(s, (self.x - (s.get_width() / 2), self.y - (s.get_height() / 2)))
	
	def isHit(self, rect):
		if self.animation.getComa() < 8:
			return rect.colliderect(self.rect_hit.move(self.x, self.y))
		else:
			return False
