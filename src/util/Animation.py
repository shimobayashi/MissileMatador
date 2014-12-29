#(C) Akimasa 2006

class Animation:
	def __init__(self, surface, areas, wait, loop):
		self.surface = surface
		self.areas = areas
		self.wait = wait
		self.loop = loop
		self.coma = 0
		self.count = 0
		self.finish = False
	
	def update(self, seek = 1):
		self.count += seek
		self.coma = int(self.count / self.wait)
		if self.coma >= len(self.areas):
			if self.loop:
				self.coma %= len(self.areas)
			else:
				self.coma = len(self.areas) - 1
				self.finish = True
	
	def getSurface(self):
		return self.surface
	
	def getArea(self):
		return self.areas[self.coma]
	
	def isFinished(self):
		return self.finish
	
	def getComa(self):
		return self.coma
