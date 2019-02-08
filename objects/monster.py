class Monster:

	def __init__(self, x, y, room):
		self.x = x
		self.y = y

		self.room = room
		room.monsters.append(self)