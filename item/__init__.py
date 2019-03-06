from typing import Tuple


class Item:

	def __init__(self, room, x, y):
		self.room = room
		self.x = x
		self.y = y

	def render(self, detected: bool) -> str:
		pass

	def collect(self) -> Tuple[int, int, int, int, str]:
		pass
