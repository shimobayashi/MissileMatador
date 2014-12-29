#(C) Akimasa 2006

import pygame
from pygame.locals import *
from util import *
from math import *

class Matador(Actor):
	DIR_LEFT = -1
	DIR_RIGHT = 1
	
	def __init__(self, game, x, y):
		Actor.__init__(self, game)
		self.controller = self.game.controller
		self.x, self.y = x, y
		self.vx, self.vy = 0, 0
		self.on_ground = False
		self.direction = self.DIR_RIGHT
		self.fall = False
		self.rect_collision = pygame.Rect(2, 0, 12, 16)
		self.rect_hit = pygame.Rect(4, 4, 8, 8)
		self.anim_stand = Animation(self.game.images['matador'], ((0, 0, 16, 16),), 1, True)
		self.anim_run = Animation(self.game.images['matador'], ((0, 16, 16, 16), (16, 16, 16, 16), (32, 16, 16, 16), (48, 16, 16, 16)), 10, True)
		self.anim_fly = Animation(self.game.images['matador'], ((16, 32, 16, 16),), 1, True)
		self.anim_fall = Animation(self.game.images['matador'], ((16, 112, 16, 16),), 1, True)
		self.animation = self.anim_stand
	
	def update(self):
		self.doOperation()
		self.addGravity()
		self.updateVelocity()
		self.updatePosition()
		self.updateAnimation()
	
	def doOperation(self):
		if self.fall:
			return
		#Run or Stand
		if self.game.controller.buttons['left'].isPressed():
			if self.on_ground:
				self.vx -= 0.2
			else:
				self.vx -= 0.15
			self.direction = self.DIR_LEFT
			self.animation = self.anim_run
		elif self.game.controller.buttons['right'].isPressed():
			if self.on_ground:
				self.vx += 0.2
			else:
				self.vx += 0.15
			self.direction = self.DIR_RIGHT
			self.animation = self.anim_run
		else:
			self.animation = self.anim_stand
		#Jump
		if self.on_ground and self.game.controller.buttons['jump'].isDown():
			self.vy -= 3.75
	
	def addGravity(self):
		self.vy += 0.125
	
	def updatePosition(self):
		self.updatePositionX()
		self.updatePositionY()
		if self.y > 240:
			self.fall = True
	
	def updatePositionX(self):
		xx = self.x + self.vx
		rect = self.game.scene.field.collide(self.rect_collision.move(xx, self.y))
		if rect is None:
			self.x = xx
			return False
		else:
			if self.vx > 0:
				self.x = rect.x - self.rect_collision.width - self.rect_collision.x
			else:
				self.x = rect.x + rect.width - self.rect_collision.x
			self.vx = 0
			return True
	
	def updatePositionY(self):
		self.on_ground = False
		yy = ceil(self.y + self.vy)
		rect = self.game.scene.field.collide(self.rect_collision.move(self.x, yy))
		if rect is None:
			self.y = yy
			return False
		else:
			if self.vy > 0:
				self.y = rect.y - self.rect_collision.height - self.rect_collision.y
				self.on_ground = True
			else:
				self.y = rect.y + rect.height - self.rect_collision.y
			self.vy = 0
			return True
	
	def updateVelocity(self):
		self.vx *= 0.9
		self.vy *= 0.99
	
	def updateAnimation(self):
		if self.fall:
			self.animation = self.anim_fall
		elif not self.on_ground:
			self.animation = self.anim_fly
		self.animation.update()
	
	def draw(self):
		s = self.animation.getSurface().subsurface(self.animation.getArea())
		if self.direction == self.DIR_LEFT:
			s = pygame.transform.flip(s, True, False)
		self.game.display.blit(s, (self.x, self.y))
	
	def isHit(self, rect):
		return rect.colliderect(self.rect_hit.move(self.x, self.y))
	
	def hit(self):
		self.fall = True
	
	def isFall(self):
		return self.fall
