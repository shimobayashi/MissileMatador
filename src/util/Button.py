#(C) Akimasa 2006

class Button:
	def __init__(self, joystick = None):
		self.joystick = joystick
		self.prev_pressed = False
		self.down = False
		self.up = False
	
	def update(self):
		self.down = False
		self.up = False
		if not self.prev_pressed and self.isPressed():
			self.down = True
		elif self.prev_pressed and self.isReleased():
			self.up = True
		self.prev_pressed = self.isPressed()
	
	def isPressed(self):
		return False
	
	def isReleased(self):
		return not self.isPressed()
	
	def isDown(self):
		return self.down
	
	def isUp(self):
		return self.up
