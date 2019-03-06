import constants as const
import random as randLib
import util


class Monster:

	def __init__(self, x, y, room, difficulty, baseHealth):
		self.x = x
		self.y = y
		self.room = room
		self.diff = float(difficulty) / 2

		self.target = randLib.choice([i for i in range(0, 4) if room.neighbours[i] is not None])
		self.health = baseHealth * self.diff

	def move(self, prx, pry, px, py):
		"""
		:param prx: Player's room x
		:param pry: Player's room y
		:param px: Player's x
		:param py: Players y
		:return the requested movement for the monster
		"""
		if prx != self.room.x and pry != self.room.y:
			if self.target == 0:
				target = (int(const.ROOM_WIDTH / 2), 0)
			elif self.target == 1:
				target = (const.ROOM_WIDTH - 1, int(const.ROOM_HEIGHT / 2))
			elif self.target == 2:
				target = (int(const.ROOM_WIDTH / 2), const.ROOM_HEIGHT - 1)
			elif self.target == 3:
				target = (0, int(const.ROOM_HEIGHT / 2))
		else:
			target = (px, py)

		if self.x == target[0] and self.y == target[1]:
			if self.target == 0:
				return 0
			elif self.target == 1:
				return 2
			elif self.target == 2:
				return 4
			else:
				return 6

		return util.roombfs(self.x, self.y, target[0], target[1], self.room)

	def render(self):
		pass

	def hit(self, power, curse):
		self.health -= int(power)
		return self.health <= 0

	def hitmsg(self):
		pass

	def attack(self):
		pass

	def attackmsg(self):
		pass

	def killedBy(self):
		pass
