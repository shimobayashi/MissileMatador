#(C) Akimasa 2006

class ActorPool:
	def __init__(self, actors = []):
		self.actors = actors[:]
	
	def __getattr__(self, attr):
		return getattr(self.actors, attr)
	
	def update(self):
		for actor in self.actors:
			actor.update()
	
	def collide(self):
		for actor in self.actors:
			actor.collide()
	
	def draw(self):
		for actor in self.actors:
			actor.draw()
	
	def burial(self):
		self.actors = [actor for actor in self.actors if actor.isAlive()]
