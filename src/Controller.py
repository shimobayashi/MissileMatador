#(C) Akimasa 2006

import pygame
from pygame.locals import *
from util import *

class Controller:
	def __init__(self):
		if pygame.joystick.get_count() > 0:
			self.joystick = pygame.joystick.Joystick(0)
			self.joystick.init()
		else:
			self.joystick = DummyJoystick()
		self.buttons = {}
		self.buttons['left'] = ButtonLeft(self.joystick)
		self.buttons['right'] = ButtonRight(self.joystick)
		self.buttons['up'] = ButtonUp(self.joystick)
		self.buttons['down'] = ButtonDown(self.joystick)
		self.buttons['jump'] = ButtonJump(self.joystick)
	
	def update(self):
		for button in self.buttons.values():
			button.update()

class DummyJoystick:
	def get_axis(self, axis):
		return 0.0
	
	def get_button(self, button):
		return False

class ButtonLeft(Button):
	def isPressed(self):
		return pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_LEFT] or self.joystick.get_axis(0) < -0.1

class ButtonRight(Button):
	def isPressed(self):
		return pygame.key.get_pressed()[K_d] or pygame.key.get_pressed()[K_RIGHT] or self.joystick.get_axis(0) > 0.1

class ButtonUp(Button):
	def isPressed(self):
		return pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_UP] or self.joystick.get_axis(1) < -0.1

class ButtonDown(Button):
	def isPressed(self):
		return pygame.key.get_pressed()[K_s] or pygame.key.get_pressed()[K_DOWN] or self.joystick.get_axis(1) > 0.1

class ButtonJump(Button):
	def isPressed(self):
		return pygame.key.get_pressed()[K_h] or pygame.key.get_pressed()[K_z] or self.joystick.get_button(0)
