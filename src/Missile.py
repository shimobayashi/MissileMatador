#(C) Akimasa 2006

import pygame
from pygame.locals import *
from util import *
from math import *
from Smoke import Smoke
from Explosion import Explosion

class Misile(Actor):
	def __init__(self, game, x, y, speed, angle):
		Actor.__init__(self, game)
		self.x, self.y = x, y
		self.vx, self.vy = 0, 0
		self.speed = speed
		self.angle = angle
		self.count = 0
		self.rect_hit = pygame.Rect(-8, -8, 16, 16)
	
	def update(self):
		self.doOperation()
		self.updateVelocity()
		self.updatePosition()
		self.spawnSmoke()
		self.count += 1
	
	def doOperation(self):
		dx = (self.game.scene.matador.x + 8) - self.x
		dy = (self.game.scene.matador.y + 8) - self.y
		self.angle = atan2(dy, dx)
		self.vx += self.speed * cos(self.angle)
		self.vy += self.speed * sin(self.angle)
	
	def updatePosition(self):
		self.x += self.vx
		self.y += self.vy
	
	def updateVelocity(self):
		self.vx *= 0.99
		self.vy *= 0.99
	
	def spawnSmoke(self):
		if self.count % 4 == 0:
			x = self.x - 8 * cos(self.angle)
			y = self.y - 8 * sin(self.angle)
			self.game.scene.effects.append(Smoke(self.game, x, y))
	
	def collide(self):
		self.collideExplosions()
		self.collideMisiles()
		self.collideMatador()
	
	def collideExplosions(self):
		for explosion in self.game.scene.explosions[:]:
			if explosion.isHit(self.rect_hit.move(self.x, self.y)):
				self.kill()
	
	def collideMisiles(self):
		for misile in self.game.scene.misiles:
			if misile is not self:
				if misile.isHit(self.rect_hit.move(self.x, self.y)):
					self.kill()
	
	def collideMatador(self):
		if self.game.scene.matador.isHit(self.rect_hit.move(self.x, self.y)):
			self.game.scene.matador.hit()
			self.kill()
	
	def draw(self, surface):
		s = pygame.transform.rotate(surface, degrees(-self.angle))
		self.game.display.blit(s, (self.x - (s.get_width() / 2), self.y - (s.get_height() / 2)))
	
	def isHit(self, rect):
		return rect.colliderect(self.rect_hit.move(self.x, self.y))
	
	def kill(self):
		Actor.kill(self)
		self.game.scene.explosions.append(Explosion(self.game, self.x, self.y))

class GreenMisile(Misile):
	def __init__(self, game, x, y, angle):
		Misile.__init__(self, game, x, y, 0.05, angle)
	
	def draw(self):
		Misile.draw(self, self.game.images['missile_g'])

class YellowMisile(Misile):
	def __init__(self, game, x, y, angle):
		Misile.__init__(self, game, x, y, 0.075, angle)
	
	def draw(self):
		Misile.draw(self, self.game.images['missile_y'])

class RedMisile(Misile):
	def __init__(self, game, x, y, angle):
		Misile.__init__(self, game, x, y, 0.1, angle)
	
	def draw(self):
		Misile.draw(self, self.game.images['missile_r'])
