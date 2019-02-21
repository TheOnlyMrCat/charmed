import random
import render as rd
import room.definitions as bodies

def mapToOutput(c: str) -> str:
	if c == 'w':
		return rd.shallow # White '.' on bright blue
	elif c == 'W':
		return rd.water # Bright blue '~' on blue
	elif c == 'l':
		return rd.lava # Dark orange '~' on orange
	elif c == '"':
		return rd.grass # Green '"' on black
	elif c == '#':
		return rd.wall # White '#' on light brown
	else:
		return rd.blankf + c[0]

class Room:

	def __init__(self, x, y, flags, body = bodies.GENERIC):
		self.neighbours = [None, None, None, None]

		self.x = x
		self.y = y

		self.monsters = []
		self.body = random.choice(body)

		self.exit = bool(flags & 0b100)
		self.upstair = not self.exit and bool(flags & 0b010)
		self.downstair = not (self.exit or self.upstair) and bool(flags & 0b001)

		self.entryPoint = self.findEntryPoint()

	def findEntryPoint(self):
		for row in range(len(self.body)):
			for cell in range(len(self.body[row])):
				if '!' in self.body[row][cell]:
					return cell, row
		return None


	def getPrintBody(self):
		return [[mapToOutput(char) for char in row] for row in self.body]