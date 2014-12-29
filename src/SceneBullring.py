#(C) Akimasa 2006

import pygame
from pygame.locals import *
from util import *
from math import *
import glob
from Scene import Scene
from Field import Field
from Matador import Matador
from Missile import *
import SceneTitle
import SceneBonus

class SceneBullring(Scene):
	def __init__(self, game, level):
		Scene.__init__(self, game)
		self.level = level
		self.fmf = FMFLoader('data/field/%02d.fmf' % self.level)
		self.field = Field(self.game, self.fmf.getLayer(0), self.fmf.chipWidth, self.fmf.chipHeight)
		x, y = self.getStartingPointMatador(self.fmf.getLayer(1))
		self.matador = Matador(self.game, x, y)
		self.misiles = self.makeMisiles(self.fmf.getLayer(2))
		self.explosions = ActorPool()
		self.effects = ActorPool()
		self.countdown_start = 1.5 * 50
		self.countdown_finish = 1.5 * 50
		self.game.sounds['gong'].play()
	
	def getStartingPointMatador(self, layer):
		for y in range(layer.height):
			for x in range(layer.width):
				if layer.get(x, y) == 0:
					return (x * self.fmf.chipWidth, y * self.fmf.chipHeight)
	
	def makeMisiles(self, layer):
		misiles = ActorPool()
		for y in range(layer.height):
			for x in range(layer.width):
				if layer.get(x, y) != 255:
					xx = x * self.fmf.chipWidth + 8
					yy = y * self.fmf.chipHeight + 8
					dx = (self.matador.x + 8) - xx
					dy = (self.matador.y + 8) - yy
					angle = atan2(dy, dx)
					if layer.get(x, y) == 0:
						misile = GreenMisile(self.game, xx, yy, angle)
					elif layer.get(x, y) == 1:
						misile = YellowMisile(self.game, xx, yy, angle)
					elif layer.get(x, y) == 2:
						misile = RedMisile(self.game, xx, yy, angle)
					misiles.append(misile)
		return misiles
	
	def update(self):
		if self.matador.isFall():
			self.countdown_finish -= 1
			if self.countdown_finish == 0:
				self.game.scene = SceneTitle.SceneTitle(self.game, self.level)
				return
		elif len(self.misiles) == 0:
			self.countdown_finish -= 1
			if self.countdown_finish == 0:
				max_level = len(glob.glob('data/field/*.fmf')) - 1
				if self.level == max_level:
					self.game.scene = SceneBonus.SceneBonus(self.game)
				else:
					self.game.scene = SceneTitle.SceneTitle(self.game, self.level + 1)
				return
		if self.countdown_start == 0:
			#Update
			self.matador.update()
			self.misiles.update()
			self.explosions.update()
			self.effects.update()
			#Collide
			self.matador.collide()
			self.misiles.collide()
			self.explosions.collide()
			self.effects.collide()
			#Burial
			self.misiles.burial()
			self.explosions.burial()
			self.effects.burial()
		else:
			self.countdown_start -= 1
	
	def draw(self):
		self.drawBackground()
		self.field.draw()
		self.effects.draw()
		self.explosions.draw()
		self.matador.draw()
		self.misiles.draw()
	
	def drawBackground(self):
		self.game.display.blit(self.game.images['background'], (0, 0))
