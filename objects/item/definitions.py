from typing import Tuple

from objects.item import Item

import constants as const
import random as randLib

possibleItems = [
	[ # Depth 0
		0, 0, 0, 0, 0, 2, 3, 3
	],
	[ # Depth 1
		0, 0, 0, 0, 0, 1, 2, 2, 3, 3, 3
	],
	[ # Depth 2
		0, 1, 2, 3
	],
	[ # Depth 3
		0, 1, 2, 3
	],
	[ # Depth 4
		0, 1, 2, 3
	],
	[ # Depth 5
		0, 1, 2, 3
	],
	[ # Depth 6
		0, 1, 2, 3
	],
	[ # Depth 7
		0, 1, 2, 3
	],
	[ # Depth 8
		0, 1, 2, 3
	],
	[ # Depth 9
		0, 1, 2, 3
	]
]

# Only here to render inside the room
class Charm(Item):

	def __init__(self, room, x, y):
		super().__init__(room, x, y)

	def render(self, detected: bool) -> str:
		return '\x1b[38;5;196m' + ('\x1b[48;5;12m' if detected else '') + '℧'

	def collect(self):
		return 0, 0, 0, 0, 'You put the charm on.', 0b10


# Item type 0
class Gold(Item):

	def __init__(self, room, x, y, value = randLib.randint(50, 150)):
		super().__init__(room, x, y)
		self.value = value

	def render(self, detected):
		return '\x1b[0;93;40m*' if not detected else '\x1b[0;93;104m*'

	def collect(self):
		return 0, 0, 0, self.value, 'You got ' + str(self.value) + ' gold', 0b0

# Item type 1
class Chance(Item):

	def __init__(self, room, x, y, depth):
		super().__init__(room, x, y)

		if x is not const.ROOM_WIDTH - 1:
			room.items[(x + 1, y)] = Gold(room, x + 1, y)
		if x is not 0:
			room.items[(x - 1, y)] = Gold(room, x - 1, y)
		if y is not const.ROOM_HEIGHT - 1:
			room.items[(x, y + 1)] = Gold(room, x, y + 1)
		if y is not 0:
			room.items[(x, y - 1)] = Gold(room, x, y - 1)

		self.health = 0
		self.armour = 0
		self.attack = 0

		self.badOrGood = randLib.randint(0, 100) < 50

		stat = randLib.randint(0, 2)

		if stat is 0:
			self.health = (-randLib.randint(0, 10) if self.badOrGood is False else randLib.randint(0, 10)) * depth
		elif stat is 1:
			self.armour = (-randLib.randint(0, 10) if self.badOrGood is False else randLib.randint(0, 10)) * depth
		elif stat is 2:
			self.attack = (-randLib.randint(0, 10) if self.badOrGood is False else randLib.randint(0, 10)) * depth

	def render(self, detected):
		return '\x1b[0;97;' + ('40' if not detected else '104' if self.badOrGood else '31') + 'm\x1b[38;5;' + str(randLib.randint(16, 231)) + 'm‽'

	def collect(self):
		return self.health, self.armour, self.attack, 0, 'You feel a ' + ('ben' if self.badOrGood else 'mal') + 'evolent force  wash over you', 0b00

# Item type 2
class Detector(Item):

	def __init__(self, room, x, y):
		super().__init__(room, x, y)

	def render(self, detected):
		return '\x1b[0;97;104m√'

	def collect(self):
		return 0, 0, 0, -50, 'You notice the presence of items on the level', 0b01

# Item type 3
class Boost(Item):

	def __init__(self, room, x, y, depth):
		super().__init__(room, x, y)

		self.health = 0
		self.armour = 0
		self.attack = 0

		stat = randLib.randint(0, 2)
		if stat is 0:
			self.health = randLib.randint(1, depth + 1) * 10
			self.message = 'You feel a lot better'
		elif stat is 1:
			self.armour = randLib.randint(1, depth + 1) * 5
			self.message = 'You feel your skin harden, and fear damage less'
		elif stat is 2:
			self.attack = randLib.randint(1, depth + 1) * 5
			self.message = 'You feel a lot stronger'

	def render(self, detected):
		return ('\x1b[0;31;40m' if not detected else '\x1b[0;97;104m')\
		+ (	'♥' if self.health is not 0 else
			'✚' if self.armour is not 0 else
			'♠︎')

	def collect(self):
		return self.health, self.armour, self.attack, 0, self.message, 0b00