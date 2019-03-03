from typing import Dict, Tuple
from objects.item import Item
from objects.monster import Monster

import constants as const
import random
import render as rd
import room.definitions as bodies

BLOCKING = ['#', "#p", 'W', 'l']


def mapToOutput(d: str) -> str:
	c = d[0]
	if c == '.':
		return rd.floor
	elif c == 'w':
		return rd.shallow
	elif c == 'W':
		return rd.water
	elif c == 'l':
		return rd.lava
	elif c == '"':
		return rd.grass
	elif c == '#':
		return rd.wall
	elif c == '#p':
		return rd.pillar
	elif c == ',':
		return rd.rubble
	else:
		return rd.blankf + c


class Room:

	def __init__(self, x, y, body=bodies.GENERIC):
		self.neighbours = [None, None, None, None]

		self.x = x
		self.y = y

		self.items: Dict[Tuple[int, int], Item] = dict([])
		self.monsters: Dict[Tuple[int, int], Monster] = dict([])
		self.body = random.choice(body)

		for y in range(const.ROOM_HEIGHT):
			for x in range(const.ROOM_WIDTH):
				self.monsters[(x, y)] = None

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
