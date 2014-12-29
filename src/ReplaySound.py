import pygame
from pygame.locals import *
import sys
import os
import glob

class ReplaySound:
	def __init__(self, filename):
		pygame.init()
		display = pygame.display.set_mode((320, 240))
		self.log = self.loadLog(filename)
		print self.log
		self.sounds = self.loadSounds("data/sound/*.wav")
		print self.sounds
		self.mainloop()

	def loadLog(self, filename):
		result = []
		f = open(filename)
		lines = f.readlines()
		for line in lines:
			tmp = line.split(":")
			root = os.path.splitext(os.path.split(tmp[1])[1])[0]
			result.append([int(tmp[0]), root])
		return result

	def loadSounds(self, path):
		result = {}
		for filename in glob.glob(path):
			root, ext = os.path.splitext(os.path.split(filename)[1])
			result[root] = pygame.mixer.Sound(filename)
		return result
	
	def mainloop(self):
		frame_count = 0
		clock = pygame.time.Clock()
		#while len(self.log) > 0:
		while True:
			while len(self.log) > 0 and self.log[0][0] == frame_count:
				self.sounds[self.log[0][1]].play()
				self.log = self.log[1:]
			clock.tick(60)
			frame_count += 1

if __name__ == "__main__":
	if len(sys.argv) >= 2:
		filename = sys.argv[1]
		rs = ReplaySound(filename)
