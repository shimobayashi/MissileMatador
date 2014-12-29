#(C) Akimasa 2006

import pygame
from pygame.locals import *
from util import *
import glob
from Scene import Scene
import SceneBullring

class SceneTitle(Scene):
	MENU_LEVEL = 0
	MENU_EXIT = 1
	
	def __init__(self, game, level = 0):
		Scene.__init__(self, game)
		self.level = level
		self.pointer = self.MENU_LEVEL
		self.setupLevels()
		self.makeFonts()
	
	def setupLevels(self):
		self.max_level = len(glob.glob('data/field/*.fmf')) - 1
		self.clear_level = int(file('save.dat', 'r').read())
		self.updateClearLevel(self.level)
		self.level %= (self.clear_level + 1)
	
	def updateClearLevel(self, level):
		if level > self.clear_level:
			self.clear_level = level
		if self.clear_level > self.max_level:
			self.clear_level = self.max_level
		file('save.dat', 'w').write(str(self.clear_level))
	
	def makeFonts(self):
		s = pygame.transform.scale(self.game.images['font'], (16 * 0x10, 16 * 0x08))
		self.font16x16 = Font(s, 16, 16)
		self.surface_title = self.font16x16.render('Missile Matador')
		self.font8x8 = Font(self.game.images['font'], 8, 8)
	
	def update(self):
		#Point
		if self.game.controller.buttons['up'].isDown():
			self.pointer -= 1
		elif self.game.controller.buttons['down'].isDown():
			self.pointer += 1
		self.pointer %= 2
		#Select
		if self.game.controller.buttons['jump'].isDown():
			if self.pointer == self.MENU_LEVEL:
				self.game.scene = SceneBullring.SceneBullring(self.game, self.level)
			elif self.pointer == self.MENU_EXIT:
				self.game.kill()
		#Select Level
		if self.game.controller.buttons['left'].isDown():
			self.level -= 1
		elif self.game.controller.buttons['right'].isDown():
			self.level += 1
		self.level %= (self.clear_level + 1)
	
	def draw(self):
		self.game.display.blit(self.game.images['background'], (0, 0))
		self.game.display.blit(self.surface_title, (160 - self.surface_title.get_width() / 2, 64))
		s = self.font8x8.render('Level %02d\nExit' % (self.level + 1))
		self.game.display.blit(s, (160 - s.get_width() / 2, 160))
		self.game.display.blit(self.game.images['pointer'], (160 - s.get_width() / 2 - 8 - 2, 160 + self.pointer * 8))
