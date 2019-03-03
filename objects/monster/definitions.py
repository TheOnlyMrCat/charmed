from objects.monster import Monster

import random as randLib

possibleMonsters = [
	[0, 1],  # Depth 0
	[0, 0, 1, 1, 1],  # Depth 1
	[0, 1, 1, 2],  # Depth 2
	[1, 1, 1, 2],  # Depth 3
	[1, 1, 2, 2, 3],  # Depth 4
	[1, 2, 2, 2, 3, 3, 3],  # Depth 5
	[1, 2, 2, 3, 3, 3, 4],  # Depth 6
	[2, 2, 3, 3, 3, 4, 4],  # Depth 7
	[2, 3, 3, 3, 3, 4, 4, 4, 5],  # Depth 8
	[3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 6],  # Depth 9
]


# Type 0
class Beetle(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 0)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[38;5;90m\x1b[48;5;0mb'

	def hit(self, power):
		return True

	def hitmsg(self):
		return 'You squashed the beetle'

	def attack(self):
		return 5 * self.diff

	def attackmsg(self):
		return 'The beetle bit you'

	def killedBy(self):
		return 'Killed by a beetle'


# Type 1
class Scorpion(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 10)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[0;90;40ms'

	def hit(self, power):
		return super().hit(power / 2)

	def hitmsg(self):
		return 'You hit the scorpion'

	def attack(self):
		return 2 * self.diff

	def attackmsg(self):
		return 'The scorpion stung you'

	def killedBy(self):
		return 'Killed by a scorpion'


# Type 2
class Mummy(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 20)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[38;5;228m\x1b[48;5;0mm'

	def hit(self, power):
		return super().hit(power / 5)

	def hitmsg(self):
		return 'You hit the mummy'

	def attack(self):
		return 5 * self.diff

	def attackmsg(self):
		return randLib.choice(['The mummy slapped you', 'The mummy mauled you', 'The mummy hit you', 'The mummy kicked you'])

	def killedBy(self):
		return 'Killed by a mummy'


# Type 3
class Slave(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 30)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[38;5;215m\x1b[48;5;0mS'

	def hit(self, power):
		return super().hit(power / 7)

	def hitmsg(self):
		return 'You hit the slave'

	def attack(self):
		return 7 * self.diff

	def attackmsg(self):
		return randLib.choice(['The slave hit you', 'The slave mauled you', 'The slave bashed you', 'The slave kicked you'])

	def killedBy(self):
		return 'Killed by a slave'


# Type 4
class Pharaoh(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 50)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[38;5;208m\x1b[48;5;0mP'

	def hit(self, power):
		return super().hit(power/ 15)

	def hitmsg(self):
		return 'You hit the undead pharaoh'

	def attack(self):
		return 15 * self.diff

	def attackmsg(self):
		return 'The undead pharaoh hit you'

	def killedBy(self):
		return 'Killed by a pharaoh'


# Type 5
class Lek(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 100)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[38;5;' + str(randLib.randint(18, 231)) + 'm\x1b[48;5;0mL'

	def hit(self, power):
		return super().hit(power / 50)

	def attack(self):
		return 20 * self.diff

	def attackmsg(self):
		return randLib.choice(['The Lek rubbed you', 'The Lek dandruffed you', 'The Lek bumped you'])

	def killedBy(self):
		return 'Rubbed by Lek'


# Type 6
class Chin(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 0)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[38;5;' + str(randLib.randint(18, 231)) + 'm\x1b[48;5;0mG'

	def hit(self, power):
		return False

	def hitmsg(self):
		return 'You miss the giant chin'

	def attack(self):
		return 999999

	def attackmsg(self):
		return 'The giant chin engulfs you'

	def killedBy(self):
		return 'Engulfed by a giant chin'