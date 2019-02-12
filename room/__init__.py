import random as rd
import room.definitions as bodies

def mapToOutput(c: str) -> str:
	if c == 'w':
		return '\x1b[0;97;104m.' # White '.' on bright blue
	elif c == 'W':
		return '\x1b[0;94;44m~' # Bright blue '~' on blue
	elif c == 'l':
		return '\x1b[38;5;202m\x1b[48;5;208m~' # Dark orange '~' on orange
	elif c == '"':
		return '\x1b[0;32;40m"' # Green '"' on black
	else:
		return '\x1b[0;97;40m' + c

class Room:

	def __init__(self, x, y, flags, body = bodies.GENERIC):
		self.neighbours = [None, None, None, None]

		self.x = x
		self.y = y

		self.monsters = []
		self.body = rd.choice(body)

		self.exit = bool(flags & 0b100)
		self.upstair = not self.exit and bool(flags & 0b010)
		self.downstair = not (self.exit or self.upstair) and bool(flags & 0b001)

	def getPrintBody(self):
		return ''.join(map(lambda row: ''.join(map(mapToOutput, row)), self.body)) + '\x1b[0;97;40m'