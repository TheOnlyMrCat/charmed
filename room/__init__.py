from typing import Dict, List
from objects.item import Item

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

	def __init__(self, x, y, body = bodies.GENERIC):
		self.neighbours = [None, None, None, None]

		self.x = x
		self.y = y

		self.items: Dict[List[int, int], Item] = []
		self.body = random.choice(body)

		self.exit = self.findChar('x')
		self.upstair = self.findChar('<')
		self.downstair = self.findChar('>')

		self.entryPoint = self.findChar('!')

	def findChar(self, char):
		for row in range(len(self.body)):
			for cell in range(len(self.body[row])):
				if char in self.body[row][cell]:
					return cell, row
		return None


	def getPrintBody(self):
		return [[mapToOutput(char) for char in row] for row in self.body]