#(C) Akimasa 2006

import pygame
from pygame.locals import *
from util import *
from Scene import Scene
import SceneTitle

class SceneBonus(Scene):
	def __init__(self, game):
		Scene.__init__(self, game)
		self.font8x8 = Font(self.game.images['font'], 8, 8)
		self.count = 0
	
	def update(self):
		if self.game.controller.buttons['jump'].isDown():
			self.game.scene = SceneTitle.SceneTitle(self.game)
		self.count += 1
	
	def draw(self):
		self.game.display.blit(self.game.images['bonus'], (0, 0))
		if self.count % 60 < 30:
			s = self.font8x8.render('Push Jump Button')
			self.game.display.blit(s, (160 - s.get_width() / 2, 120 - s.get_height() / 2))
