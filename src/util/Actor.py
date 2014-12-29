#(C) Akimasa 2006

class Actor:
	def __init__(self, game):
		self.game = game
		self.alive = True
	
	def update(self):
		pass
	
	def draw(self):
		pass
	
	def collide(self):
		pass
	
	def isAlive(self):
		return self.alive
	
	def kill(self):
		self.alive = False
