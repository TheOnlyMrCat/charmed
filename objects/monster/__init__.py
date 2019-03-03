class Monster:

	def __init__(self, x, y, room):
		self.x = x
		self.y = y
		self.room = room

	def move(self, prx, pry, px, py):
		"""
		:param prx: Player's room x
		:param pry: Player's room y
		:param px: Player's x
		:param py: Players y
		:return the requested movement for the monster
		"""
		pass

	def render(self):
		pass

	def hit(self, power):
		pass

	def attack(self):
		pass

	def attackmsg(self):
		pass

	def killedBy(self):
		pass