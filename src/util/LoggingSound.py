import pygame
from pygame.locals import *

class LoggingSound(pygame.mixer.Sound):
	def __init__(self, filename, game):
		pygame.mixer.Sound.__init__(self, filename)
		self.filename = filename
		self.game = game
	
	def play(self, loops = 0, maxtime = 0):
		pygame.mixer.Sound.play(self, loops, maxtime)
		f = open("soundlog.txt", "a")
		f.write("%d:%s\n" % (self.game.frame_count, self.filename))
		f.close()
