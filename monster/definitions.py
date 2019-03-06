from monster import Monster

import random as randLib

possibleMonsters = [
	[0], # Level 0
	[0, 1],  # Level 1
	[0, 0, 1, 1, 1],  # Level 2
	[0, 1, 1, 2],  # Level 3
	[1, 1, 1, 2],  # Level 4
	[1, 1, 2, 2, 3],  # Level 5
	[1, 2, 2, 2, 3, 3, 3],  # Level 6
	[1, 2, 2, 3, 3, 3, 4],  # Level 7
	[2, 2, 3, 3, 3, 4, 4],  # Level 8
	[2, 3, 3, 3, 3, 4, 4, 4, 5],  # Level 9
	[3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 6],  # level 10
	[3, 4, 4, 4, 5, 5, 5, 6], # Level 11
	[4, 5, 5, 6, 6], # Level 12

	[7, 7, 7, 8, 8] # Depth 10
]


# Type 0
class Beetle(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 0)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[38;5;90m\x1b[48;5;0mb'

	def hit(self, power, curse):
		return True

	def hitmsg(self):
		return 'You squashed the beetle'

	def attack(self):
		return 5 * self.diff

	def attackmsg(self):
		return 'The beetle bit you'

	def killedBy(self):
		return 'Killed by a beetle'


class CursedBeetle(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 50)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[38;5;90m\x1b[48;5;15mb'

	def hit(self, power, curse):
		return super().hit(power / 30, curse)

	def hitmsg(self):
		return 'You hit the cursed beetle'

	def attack(self):
		return 5 * self.diff

	def attackmsg(self):
		return 'The cursed beetle bit you'

	def killedBy(self):
		return 'Killed by a cursed beetle'


# Type 1
class Scorpion(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 10)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[0;90;40ms'

	def hit(self, power, curse):
		return super().hit(power / (2 if not curse else 1), curse)

	def hitmsg(self):
		return 'You hit the scorpion'

	def attack(self):
		return 2 * self.diff

	def attackmsg(self):
		return 'The scorpion stung you'

	def killedBy(self):
		return 'Killed by a scorpion'

class CursedScorpion(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 50)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[0;90;107ms'

	def hit(self, power, curse):
		return super().hit(power / 30, curse)

	def hitmsg(self):
		return 'You hit the cursed scorpion'

	def attack(self):
		return 5 * self.diff

	def attackmsg(self):
		return 'The cursed scorpion stung you'

	def killedBy(self):
		return 'Killed by a cursed scorpion'


# Type 2
class Mummy(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 20)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[38;5;228m\x1b[48;5;0mm'

	def hit(self, power, curse):
		return super().hit(power / (5 if not curse else 1), curse)

	def hitmsg(self):
		return 'You hit the mummy'

	def attack(self):
		return 5 * self.diff

	def attackmsg(self):
		return randLib.choice(['The mummy slapped you', 'The mummy mauled you', 'The mummy hit you', 'The mummy kicked you'])

	def killedBy(self):
		return 'Killed by a mummy'


class CursedMummy(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 50)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[38;5;228m\x1b[48;5;15mm'

	def hit(self, power, curse):
		return super().hit(power / 30, curse)

	def hitmsg(self):
		return 'You hit the cursed mummy'

	def attack(self):
		return 5 * self.diff

	def attackmsg(self):
		return randLib.choice(['The cursed mummy slapped you', 'The cursed mummy mauled you', 'The cursed mummy hit you', 'The cursed mummy kicked you'])

	def killedBy(self):
		return 'Killed by a cursed mummy'

# Type 3
class Slave(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 30)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[38;5;215m\x1b[48;5;0mS'

	def hit(self, power, curse):
		return super().hit(power / (7 if not curse else 1), curse)

	def hitmsg(self):
		return 'You hit the slave'

	def attack(self):
		return 7 * self.diff

	def attackmsg(self):
		return randLib.choice(['The slave hit you', 'The slave mauled you', 'The slave bashed you', 'The slave kicked you'])

	def killedBy(self):
		return 'Killed by a slave'

class CursedSlave(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 50)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[38;5;215m\x1b[48;5;0mS'

	def hit(self, power, curse):
		return super().hit(power / 30, curse)

	def hitmsg(self):
		return 'You hit the cursed slave'

	def attack(self):
		return 5 * self.diff

	def attackmsg(self):
		return randLib.choice(['The cursed slave hit you', 'The cursed slave mauled you', 'The cursed slave bashed you', 'The cursed slave kicked you'])

	def killedBy(self):
		return 'Killed by a cursed mummy'


# Type 4
class Pharaoh(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 50)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[38;5;208m\x1b[48;5;0mP'

	def hit(self, power, curse):
		return super().hit(power / (15 if not curse else 1), curse)

	def hitmsg(self):
		return 'You hit the undead pharaoh'

	def attack(self):
		return 15 * self.diff

	def attackmsg(self):
		return 'The undead pharaoh hit you'

	def killedBy(self):
		return 'Killed by a pharaoh'


# Type 5
class Sand(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 70)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[38;5;' + str(randLib.randint(18, 231)) + 'm\x1b[48;5;0mL'

	def hit(self, power, curse):
		return super().hit(power / (20 if not curse else 1), curse)

	def hitmsg(self):
		return "You hit the sand monster"

	def attack(self):
		return 20 * self.diff

	def attackmsg(self):
		return randLib.choice(['The sand monster winded you', 'The sand monster hit you'])

	def killedBy(self):
		return 'Killed by sand'


# Type 6
class Warden(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 100)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[38;5;196m\x1b[48;5;0mC'

	def hit(self, power, curse):
		return super().hit(power / (30 if not curse else 1), curse)

	def hitmsg(self):
		return 'You hit the charmed warden'

	def attack(self):
		return 30 * self.diff

	def attackmsg(self):
		return 'The charmed warden struck you'

	def killedBy(self):
		return 'Avenged by a charmed guardian'

# Type 7
class Guardian(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 100)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[0;35;40mg'

	def hit(self, power, curse):
		return super().hit(power / (30 if not curse else 1), curse)

	def hitmsg(self):
		return 'You hit the cursed guardian'

	def attack(self):
		return 30 * self.diff

	def attackmsg(self):
		return randLib.choice(['The cursed guardian struck you', 'The cursed guardian cut you'])

	def killedBy(self):
		return 'Avenged by a cursed guardian'

# Type 8
class Winged(Monster):

	def __init__(self, x, y, room, difficulty):
		super().__init__(x, y, room, difficulty, 100)

	def move(self, prx, pry, px, py):
		return super().move(prx, pry, px, py)

	def render(self):
		return '\x1b[0;34;40mW'

	def hit(self, power, curse):
		return super().hit(power / (35 if not curse else 1), curse)

	def hitmsg(self):
		return 'You hit the winged guardian'

	def attack(self):
		return 35 * self.diff

	def attackmsg(self):
		return randLib.choice(['The winged guardian struck you', 'The winged guardian cut you'])

	def killedBy(self):
		return 'Avenged by a winged guardian'