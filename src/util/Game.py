#(C) Akimasa 2006

import pygame
from pygame.locals import *
import os
import glob
from LoggingSound import LoggingSound

class Game:
	def __init__(self, replay):
		pygame.init()
		self.replay = replay
		self.alive = True
	
	def run(self):
		self.start()
		self.loop()
		self.finish()
	
	def start(self):
		pass
	
	def loop(self):
		self.clock = pygame.time.Clock()
		while self.isAlive():
			events = pygame.event.get()
			for event in events:
				if event.type == QUIT:
					return
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					return
			self.update()
			self.draw()
			self.clock.tick(50)
	
	def update(self):
		pass
	
	def draw(self):
		pass
	
	def finish(self):
		pass
	
	def loadImages(self, path):
		result = {}
		for filename in glob.glob(path):
			root, ext = os.path.splitext(os.path.split(filename)[1])
			result[root] = pygame.image.load(filename).convert_alpha()
		return result
	
	def loadSounds(self, path):
		result = {}
		for filename in glob.glob(path):
			root, ext = os.path.splitext(os.path.split(filename)[1])
			if self.replay:
				result[root] = LoggingSound(filename, self)
			else:
				result[root] = pygame.mixer.Sound(filename)
		return result
	
	def isAlive(self):
		return self.alive
	
	def kill(self):
		self.alive = False
