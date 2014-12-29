#(C) Akimasa 2006

import pygame
from pygame.locals import *
from util import *

class Field:
	def __init__(self, game, layer, chipWidth, chipHeight):
		self.game = game
		self.layer = layer
		self.chipWidth = chipWidth
		self.chipHeight = chipHeight
		self.rects_collision = self.makeRectsCollision(self.layer)
	
	def makeRectsCollision(self, layer):
		rects = []
		for y in range(layer.height):
			for x in range(layer.width):
				if layer.get(x, y) == 0:
					rects.append(pygame.Rect(x * self.chipWidth, y * self.chipHeight, self.chipWidth, self.chipHeight))
		return rects
	
	def draw(self):
		for y in range(self.layer.height):
			for x in range(self.layer.width):
				if self.layer.get(x, y) == 0:
					self.game.display.blit(self.game.images['block'], (x * self.chipWidth, y * self.chipHeight))
	
	def collide(self, rect):
		index = rect.collidelist(self.rects_collision)
		if index == -1:
			return None
		else:
			return self.rects_collision[index]
