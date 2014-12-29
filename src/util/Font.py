#(C) Akimasa 2006

import pygame
from pygame.locals import *
import string

class Font:
	def __init__(self, surface, width, height):
		self.surface = surface
		self.width = width
		self.height = height
	
	def render(self, str):
		lines = string.split(str, '\n')
		max = 0
		for line in lines:
			if len(line) > max:
				max = len(line)
		width = max * self.width
		height = len(lines) * self.height
		surface = pygame.Surface((width, height))
		surface.set_colorkey((0, 0, 0))
		surface = surface.convert_alpha()
		x, y = 0, 0
		for line in lines:
			for c in line:
				n = ord(c) - 0x20
				u = n % 16 * self.width
				v = n / 16 * self.height
				area = (u, v, self.width, self.height)
				surface.blit(self.surface, (x, y), area)
				x += self.width
			x = 0
			y += self.height
		return surface.convert_alpha()
