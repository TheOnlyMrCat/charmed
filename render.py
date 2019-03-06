from typing import List

import math
import constants as const
import subprocess

from room import Room

blankf = '\x1b[0;97;40m'
floor = blankf + '.'

wallf = '\x1b[38;5;15m\x1b[48;5;136m'
wall = wallf + '#'

pillarf = '\x1b[38;5;235m\x1b[48;5;245m'
pillar = pillarf + '#'

shallowf = '\x1b[0;97;46m'
shallow = shallowf + '.'

waterf = '\x1b[0;94;44m'
water = waterf + '~'

lavaf = '\x1b[38;5;202m\x1b[48;5;208m'
lava = lavaf + '~'

grassf = '\x1b[0;32;40m'
grass = grassf + '"'

rubblef = blankf
rubble = rubblef + '⢕'

playerf = '\x1b[0;33;40m'
player = playerf + '@'

detectf = '\x1b[0;30;107m'

stairf = '\x1b[0;33;103m'
downstair = stairf + '>'
upstair = stairf + '<'

exitf = '\x1b[0;35;105m'
exit = exitf + 'H'


def welcome():
	header()
	print('Welcome to charmed.')
	print('Ensure your terminal window is full-screen.')
	print('When the game starts, do not switch to another window without suspending the game by pressing "p"')
	return input('Input options, then press enter to continue: ')


def difficulty():
	header()
	print('Difficulty: [1] I wanna go home! (Monsters have less health and attack, and helpful items spawn more frequently')
	print("            [2] What's in here? (Recommended)")
	print('            [3] Hurt me plenty! (Monsters have more health and attack, and harmful items spawn more frequently)')
	print("            [4] Just kill me. (Monsters have more health and attack, and helpful items are extremely rare")
	return int(input('Input a value: '))


def seed():
	header()
	return input('Seed: ')


def generating(seedVal=None):
	header()
	print('Generating level' + (('with seed ' + seedVal) if seedVal is not None else '') + '. This will take a moment.')


def tutorial():
	header()
	print('Your mission is to acquire the Charm of Relativity from the ninth layer and return with it to the drop zone.')
	print('This is a dangerous mission, and you are likely to die on the way.')
	print("We can revive you, but we can't drop you in the same dungeon twice.")
	print('Be careful. Strange things lurk beneath the surface.')
	print()
	print('Good luck.')
	print()
	print('You are represented by "' + player + blankf + '".')
	print('Press "?" at any time for help.')
	input('Press enter to continue.')


def commands():
	header()
	print('          \x1b[48;5;91my\x1b[48;5;196mk\x1b[38;5;0m\x1b[48;5;208mu')
	print(blankf + 'Movement: \x1b[48;5;21mh\x1b[0;97;40m \x1b[38;5;0m\x1b[48;5;226ml\x1b[0;97;40m')
	print('          \x1b[48;5;29mb\x1b[38;5;0m\x1b[48;5;46mj\x1b[48;5;154mn\x1b[0;97;40m')
	print()
	print('          \x1b[48;5;91my\x1b[48;5;208mu\x1b[0;97;40m')
	print('          \x1b[48;5;21mh\x1b[38;5;0m\x1b[48;5;46mj\x1b[38;5;15m\x1b[48;5;196mk\x1b[38;5;0m\x1b[48;5;226ml\x1b[0;97;40m')
	print('          \x1b[48;5;29mb\x1b[38;5;0m\x1b[48;5;154mn')
	print(blankf + "WASD also works, but doesn't support diagonal movement")
	print('Press "z" to skip moving for the turn')
	print()
	print('Commands: q: Quit game')
	print('          p: Suspend game')
	print()
	print(': <enter>: input long commands:')
	print('          "seed": Show game seed')
	print('          "difficulty": Show game difficulty')
	print()
	print('Options for startup text: "\'" to skip tutorial')
	print('                          "d" to set difficulty')
	print('                          "s" to set seed')
	print('                          "h" to show highscores and exit')
	input('Press enter to continue.')


def suspend():
	header()
	print('Game suspended.')
	input('Press enter to continue.')


def header():
	subprocess.call('clear')
	print(blankf + '', end='')
	print('=============== Charmed ===============')


def stats(health, dhealth, attack, dattack, armour, darmour, score, dscore, charm):
	print('Health: ', end='')
	print('♥' * int(max(health / 5, 1)), end='')
	if dhealth != 0:
		print('(+' + str(dhealth) + ')')
	else:
		print()

	print('Armour: ', end='')
	print('✚' * int(max(armour / 5, 1)), end='')
	if darmour != 0:
		print('(+' + str(darmour) + ')')
	else:
		print()

	print('Attack: ', end='')
	print('♠︎' * int(max(attack / 5, 1)), end='')
	if dattack != 0:
		print('(+' + str(darmour) + ')')
	else:
		print()

	print('Score:', score, end='')
	print('℧' if charm else '', end='')
	if dscore > 0:
		print('(+' + str(dscore) + ')')
	else:
		print()


def rooms(roomMap: List[List[int]], pos: List[int]):
	"""
	The list is a list of bytes where each bit is significant.
	Byte: ixudnesw
	i: Whether the tile contains a detected object
	x: Whether the tile contains the dungeon's exit
	u: Whether the tile contains an upward staircase
	d: Whether the tile contains a downward staircase
	n: Whether the tile has a northern exit
	e: Whether the tile has an eastern exit
	s: Whether the tile has a southern exit
	W: Whether the tile has a western exit

	To show an unexplored room, set all bits to 0
	"""
	print()
	print('Map:')
	print(wallf + ('#' * (const.MAP_WIDTH + 2)))

	for y in range(len(roomMap)):
		print(wall, end='')
		for x in range(len(roomMap[y])):
			if x == pos[0] and y == pos[1]:
				print(player, end='')
				continue

			c = roomMap[y][x]

			if c & 0b10000000:
				print(detectf, end='')
			else:
				print(blankf, end='')

			if c & 0b01000000:
				print(exit, end='')
			elif c & 0b00100000:
				print(upstair, end='')
			elif c & 0b00010000:
				print(downstair, end='')
			else:
				n = bool(c & 0b00001000)
				e = bool(c & 0b00000100)
				s = bool(c & 0b00000010)
				w = bool(c & 0b00000001)
				if n:
					if e:
						if s:
							if w:
								print('┼', end='')  # N,E,S,W
							else:
								print('├', end='')  # N,E,S
						else:
							if w:
								print('┴', end='')  # N,E,W
							else:
								print('└', end='')  # N,E
					else:
						if s:
							if w:
								print('┤', end='')  # N,S,W
							else:
								print('│', end='')  # N,S
						else:
							if w:
								print('┘', end='')  # N,W
							else:
								print('│', end='')  # N
				elif e:
					if s:
						if w:
							print('┬', end='')  # E,S,W
						else:
							print('┌', end='')  # E,S
					else:
						if w:
							print('─', end='')  # E,W
						else:
							print('─', end='')  # E

				elif s:
					if w:
						print('┐', end='')  # S,W
					else:
						print('│', end='')  # S

				elif w:
					print('─', end='')  # W

				else:
					print(' ', end='')  # Unexplored/Nonexistent
		print(wall)

	print(wallf + ('#' * (const.MAP_WIDTH + 2)) + blankf)


def room(printRoom: Room, detected, playerPos: List[int]):
	roomChars = printRoom.getPrintBody()
	roomChars[playerPos[1]][playerPos[0]] = player

	for x in range(math.ceil(const.ROOM_WIDTH / 2)):
		print(wall, end='')
	print(floor if printRoom.neighbours[0] is not None else wall, end='')
	for x in range(math.ceil(const.ROOM_WIDTH / 2)):
		print(wall, end='')
	print()

	exitPrinted = False

	for y in range(len(roomChars)):
		print(floor if printRoom.neighbours[3] is not None and (y > const.ROOM_HEIGHT / 2 - 1 and not exitPrinted) else wall, end='')
		for x in range(len(roomChars[y])):
			print((roomChars[y][x] if (x, y) not in printRoom.items else printRoom.items[(x, y)].render(detected)) if printRoom.monsters[(x, y)] is None else printRoom.monsters[(x, y)].render(), end='')
		print(floor if printRoom.neighbours[1] is not None and (y > const.ROOM_HEIGHT / 2 - 1 and not exitPrinted) else wall)
		if y > const.ROOM_HEIGHT / 2 - 1:
			exitPrinted = True

	for x in range(math.ceil(const.ROOM_WIDTH / 2)):
		print(wall, end='')
	print(floor if printRoom.neighbours[2] is not None else wall, end='')
	for x in range(math.ceil(const.ROOM_WIDTH / 2)):
		print(wall, end='')

	print(blankf)


def highscores(scores):
	header()
	print('Highscores')
	for score in scores: print(score[0], 'with', score[1], 'gold')
	input('Press enter to continue.')


def thankyou():
	header()
	print('Thanks for playing!')
	print()


def reallyquit():
	return input('Really quit (y/n)? ') == 'y'

def cont():
	return input('Play again (y/n)? ') == 'y'