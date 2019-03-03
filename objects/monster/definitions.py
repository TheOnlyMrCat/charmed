from typing import Tuple
from objects.monster import Monster

import util
import constants as const
import random as randLib

possibleMonsters = [
	[0], # Depth 0
	[0], # Depth 1
	[0], # Depth 2
	[0], # Depth 3
	[0], # Depth 4
	[0], # Depth 5
	[0], # Depth 6
	[0], # Depth 7
	[0], # Depth 8
	[0], # Depth 9
]

# Type 0
class Beetle(Monster):

	def __init__(self, x, y, room):
		super().__init__(x, y, room)

		self.target = randLib.choice([i for i in range(0, 4) if room.neighbours[i] is not None])

	def move(self, prx, pry, px, py):
		target: Tuple[int, int]
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
		return '\x1b[38;5;90m\x1b[48;5;0mb'

	def hit(self, power):
		return True

	def attack(self):
		return 5

	def attackmsg(self):
		return 'The beetle bit you'

	def killedBy(self):
		return 'Killed by a beetle'