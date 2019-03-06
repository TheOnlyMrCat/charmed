from typing import Tuple

from room import BLOCKING

from item import Item

import constants as const
import random as randLib

possibleItems = [
	[  # Difficulty 1
		[  # Depth 0
			0, 0, 0, 0, 2, 3, 3, 5
		],
		[  # Depth 1
			0, 0, 0, 0, 0, 2, 2, 3, 3, 3, 5
		],
		[  # Depth 2
			0, 0, 0, 0, 0, 1, 2, 2, 2, 3, 3, 3, 5
		],
		[  # Depth 3
			0, 0, 0, 0, 1, 2, 2, 3, 3, 3, 3, 5
		],
		[  # Depth 4
			0, 0, 0, 0, 1, 2, 3, 3, 3, 3, 3, 4, 5
		],
		[  # Depth 5
			0, 0, 0, 0, 1, 2, 3, 3, 3, 3, 3, 4, 4, 5
		],
		[  # Depth 6
			0, 0, 0, 0, 1, 2, 3, 3, 3, 3, 3, 4, 4
		],
		[  # Depth 7
			0, 0, 0, 0, 1, 2, 3, 3, 3, 3, 3, 4, 4
		],
		[  # Depth 8
			0, 0, 0, 1, 2, 3, 3, 3, 3, 4, 4
		],
		[  # Depth 9
			0, 0, 0, 1, 2, 3, 3, 3, 3, 4, 4
		],
		[-1] # No depth 10
	],
	[  # Difficulty 2
		[  # Depth 0
			0, 0, 0, 0, 0, 2, 3, 3, 5
		],
		[  # Depth 1
			0, 0, 0, 0, 0, 1, 2, 2, 3, 3, 3, 5
		],
		[  # Depth 2
			0, 0, 0, 0, 1, 2, 2, 2, 3, 3, 3, 5
		],
		[  # Depth 3
			0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 3, 4, 5
		],
		[  # Depth 4
			0, 0, 0, 0, 1, 1, 2, 3, 3, 3, 3, 4, 5
		],
		[  # Depth 5
			0, 0, 0, 0, 1, 1, 2, 3, 3, 3, 3, 4
		],
		[  # Depth 6
			0, 0, 0, 0, 0, 1, 1, 2, 3, 3, 3, 3, 4, 4
		],
		[  # Depth 7
			0, 0, 0, 0, 1, 1, 1, 3, 3, 3, 3, 4, 4
		],
		[  # Depth 8
			0, 0, 0, 0, 1, 1, 3, 3, 3, 3, 4, 4
		],
		[  # Depth 9
			0, 0, 0, 0, 1, 1, 3, 3, 3, 4, 4, 4
		],
		[-1] # No depth 10
	],
	[  # Difficulty 3
		[  # Depth 0
			0, 0, 0, 0, 0, 2, 3, 3, 5
		],
		[  # Depth 1
			0, 0, 0, 0, 0, 1, 2, 2, 3, 3, 5
		],
		[  # Depth 2
			0, 0, 0, 0, 1, 2, 2, 3, 3, 4, 5
		],
		[  # Depth 3
			0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 5
		],
		[  # Depth 4
			0, 0, 0, 0, 1, 1, 2, 3, 3, 3, 4
		],
		[  # Depth 5
			0, 0, 0, 0, 1, 1, 2, 3, 3, 3, 4, 4
		],
		[  # Depth 6
			0, 0, 0, 0, 0, 1, 1, 2, 3, 3, 4, 4
		],
		[  # Depth 7
			0, 0, 0, 0, 1, 1, 3, 3, 3, 4, 4, 4
		],
		[  # Depth 8
			0, 0, 0, 0, 1, 1, 3, 3, 4, 4, 4
		],
		[  # Depth 9
			0, 0, 0, 0, 1, 1, 3, 4, 4, 4
		],
		[-1] # No depth 10
	],
	[  # Difficulty 4
		[  # Depth 0
			0, 0, 0, 0, 0, 0, 0, 3, 5
		],
		[  # Depth 1
			0, 0, 0, 0, 0, 0, 1, 1, 3, 4, 5
		],
		[  # Depth 2
			0, 0, 0, 0, 0, 0, 1, 3, 4, 4, 5
		],
		[  # Depth 3
			0, 0, 0, 0, 0, 1, 3, 4, 4
		],
		[  # Depth 4
			0, 0, 0, 0, 0, 1, 3, 4, 4
		],
		[  # Depth 5
			0, 0, 0, 0, 0, 1, 3, 4, 4, 4
		],
		[  # Depth 6
			0, 0, 0, 0, 0, 1, 3, 4, 4, 4
		],
		[  # Depth 7
			0, 0, 0, 0, 0, 1, 3, 4, 4, 4
		],
		[  # Depth 8
			0, 0, 0, 0, 1, 3, 4, 4, 4
		],
		[  # Depth 9
			0, 0, 0, 0, 1, 3, 4, 4, 4
		],
		[-1, -1, -1, -1, 1] # Depth 10
	],
]


# Only here to render inside the room
class Charm(Item):

	def __init__(self, room, x, y):
		super().__init__(room, x, y)

	def render(self, detected: bool) -> str:
		return '\x1b[38;5;196m\x1b[48;5;0m℧'

	def collect(self):
		return 0, 0, 0, 0, 'You put the charm on.', 0b00010


# Same as Charm
class Cursed(Item):

	def __init__(self, room, x, y):
		super().__init__(room, x, y)

	def render(self, detected: bool) -> str:
		return '\x1b[38;5;54m\x1b[48;5;0m➹'

	def collect(self):
		return 0, 0, 0, 0, 'You pick up the cursed sword', 0b00100


# Item type 0
class Gold(Item):

	def __init__(self, room, x, y, value=randLib.randint(50, 150)):
		super().__init__(room, x, y)
		self.value = value

	def render(self, detected):
		return '\x1b[0;93;40m*' if not detected else '\x1b[0;93;104m*'

	def collect(self):
		return 0, 0, 0, self.value, 'You got ' + str(self.value) + ' gold', 0b00000


# Item type 1
class Chance(Item):

	def __init__(self, room, x, y, depth, difficulty):
		super().__init__(room, x, y)

		if x is not const.ROOM_WIDTH - 1 and room.body[y][x + 1] not in BLOCKING:
			room.items[(x + 1, y)] = Gold(room, x + 1, y)
		if x is not 0 and room.body[y][x - 1] not in BLOCKING:
			room.items[(x - 1, y)] = Gold(room, x - 1, y)
		if y is not const.ROOM_HEIGHT - 1 and room.body[y + 1][x] not in BLOCKING:
			room.items[(x, y + 1)] = Gold(room, x, y + 1)
		if y is not 0 and room.body[y - 1][x] not in BLOCKING:
			room.items[(x, y - 1)] = Gold(room, x, y - 1)

		self.health = 0
		self.armour = 0
		self.attack = 0

		self.badOrGood = (randLib.randint(0, 10) + 2 - difficulty) < 5

		stat = randLib.randint(0, 2)

		if stat is 0:
			self.health = (-randLib.randint(0, 5) if self.badOrGood is False else randLib.randint(0, 5)) * depth
		elif stat is 1:
			self.armour = (-randLib.randint(0, 5) if self.badOrGood is False else randLib.randint(0, 5)) * depth
		elif stat is 2:
			self.attack = (-randLib.randint(0, 5) if self.badOrGood is False else randLib.randint(0, 5)) * depth

	def render(self, detected):
		return '\x1b[0;97;' + ('40' if not detected else '104' if self.badOrGood else '31') + 'm\x1b[38;5;' + str(randLib.randint(16, 231)) + 'm‽'

	def collect(self):
		return self.health, self.armour, self.attack, 0, 'You feel a ' + ('ben' if self.badOrGood else 'mal') + 'evolent force  wash over you', 0b00000


# Item type 2
class Detector(Item):

	def __init__(self, room, x, y):
		super().__init__(room, x, y)

	def render(self, detected):
		return '\x1b[0;97;104m√'

	def collect(self):
		return 0, 0, 0, -50, 'You notice the presence of items on the level', 0b00001


# Item type 3
class Boost(Item):

	def __init__(self, room, x, y, depth):
		super().__init__(room, x, y)

		self.health = 0
		self.armour = 0
		self.attack = 0

		stat = randLib.randint(0, 2)
		if stat is 0:
			self.health = randLib.randint(1, depth + 1) * 2
			self.message = 'You feel healthier'
		elif stat is 1:
			self.armour = randLib.randint(1, depth + 1)
			self.message = 'You feel your skin harden, and your fear of monsters decreases'
		elif stat is 2:
			self.attack = randLib.randint(1, depth + 1)
			self.message = 'You feel stronger and more willing to attack creatures'

	def render(self, detected):
		return ('\x1b[0;31;40m' if not detected else '\x1b[0;97;104m') \
			   + ('♥' if self.health is not 0 else
				  '✚' if self.armour is not 0 else
				  '♠︎')

	def collect(self):
		return self.health, self.armour, self.attack, 0, self.message, 0b00000


# Item type 4
class MonsterTrap(Item):

	def __init__(self, room, x, y):
		super().__init__(room, x, y)

	def render(self, detected: bool) -> str:
		return '\x1b[38;5;' + ('234' if not detected else '9') + 'm\x1b[48;5;0m▣'

	def collect(self):
		return 0, 0, 0, 0, 'You hear a click and monsters begin to rise from the floor!', 0b01000


# Item type 5
class Drop(Item):

	def __init__(self, room, x, y):
		super().__init__(room, x, y)

	def render(self, detected: bool) -> str:
		return '\x1b[0;97;40m◎'

	def collect(self):
		return 0, 0, 0, 0, 'You fall through a hole in the floor!', 0b10000
