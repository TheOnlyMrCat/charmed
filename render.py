from typing import List

import math
import constants as const
import subprocess

from room import Room

blankf = '\x1b[0;97;40m'
floor = blankf + '.'

wallf = '\x1b[38;5;15m\x1b[48;5;215m'
wall = wallf + '#'

shallowf = '\x1b[0;97;46m'
shallow = shallowf + '.'

waterf = '\x1b[0;94;44m'
water = waterf + '~'

lavaf = '\x1b[38;5;202m\x1b[48;5;208m'
lava = lavaf + '~'

grassf = '\x1b[0;32;40m'
grass = grassf + '"'

playerf = '\x1b[0;33;40m'
player = playerf + '@'

itemf = '\x1b[0;30;107m'

stairf = '\x1b[0;33;103m'
downstair = stairf + '>'
upstair = stairf + '<'

exitf = '\x1b[0;35;105m'
exit = exitf + 'X'


def welcome():
	header()
	print('Welcome to charmed.')
	print('Ensure your terminal window is full-screen.')
	print('When the game starts, do not switch to another window without suspending the game by pressing "s"')
	return input('Press enter to continue. ')

def difficulty():
	header()
	print('Difficulty: [1] I wanna go home! (Monsters have less health and attack, and helpful items spawn more frequently')
	print("            [2] What's in here? (Recommended)")
	print('            [3] Hurt me plenty! (Monsters have more health and attack, and harmful items spawn more frequently)')
	print("            [4] Just kill me. (Monsters have more health and attack, and helpful items don't spawn")
	return input('Input a value: ')

def seed():
	header()
	return input('Seed: ')

def generating(seedVal = None):
	header()
	print('Generating level' + (('with seed ' + seedVal) if seedVal is not None else '') + '. This will take a moment.')

def tutorial():
	header()
	print('          \x1b[48;5;91my\x1b[48;5;196mk\x1b[38;5;0m\x1b[48;5;208mu')
	print(blankf + 'Movement: \x1b[48;5;21mh\x1b[0;97;40m \x1b[38;5;0m\x1b[48;5;226ml\x1b[0;97;40m')
	print('          \x1b[48;5;29mb\x1b[38;5;0m\x1b[48;5;46mj\x1b[48;5;154mn\x1b[0;97;40m')
	print()
	print('          \x1b[48;5;91my\x1b[48;5;208mu\x1b[0;97;40m')
	print('          \x1b[48;5;21mh\x1b[38;5;0m\x1b[48;5;46mj\x1b[38;5;15m\x1b[48;5;196mk\x1b[38;5;0m\x1b[48;5;226ml\x1b[0;97;40m')
	print('          \x1b[48;5;29mb\x1b[38;5;0m\x1b[48;5;154mn')
	print(blankf + '')
	print('Press "?" at any time for help.')
	print('Commands on startup text: "\'" to skip tutorial')
	print('                          "d" to set difficulty')
	print('                          "s" to set seed')
	print()
	input('Press enter to continue.')

def suspend():
	header()
	print('Game suspended.')
	input('Press enter to continue.')

def header():
	subprocess.call('clear')
	print(blankf + '', end='')
	print('=============== Charmed ===============')

def stats(health, armour, attack, score, charm):
	print('Health: ', end='')
	print('♥' * int(max(health / 10, 1)))

	print('Armour: ', end='')
	print('✚' * int(max(armour / 10, 1)))

	print('Attack: ', end='')
	print('♠︎' * int(max(attack / 10, 1)))

	print('Score:', score, end='')
	print('℧' if charm else '')

def rooms(roomMap: List[List[int]], pos: List[int]):
	"""
	The list is a list of bytes where each bit is significant.
	Byte: ixudnesw
	i: Whether the tile contains an item
	x: Whether the tile contains the dungeon's exit
	u: Whether the tile contains an upward staircase
	d: Whether the tile contains a downward staircase
	n: Whether the tile has a northern exit
	e: Whether the tile has an eastern exit
	s: Whether the tile has a southern exit
	W: Whether the tile has a western exit

	To show an unexplored room, set all bits to 0
	"""
	print('\x1b[38;5;15m\x1b[48;5;215m' + ('#' * (const.MAP_WIDTH + 2)))

	for y in range(len(roomMap)):
		print(wall, end='')
		for x in range(len(roomMap[y])):
			if x == pos[0] and y == pos[1]:
				print(player, end='')
				continue
			
			c = roomMap[y][x]

			if c & 0b10000000:
				print(itemf, end='')
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
								print('┼', end='') # N,E,S,W
							else:
								print('├', end='') # N,E,S
						else:
							if w:
								print('┴', end='') # N,E,W
							else:
								print('└', end='') # N,E
					else:
						if s:
							if w:
								print('┤', end='') # N,S,W
							else:
								print('│', end='') # N,S
						else:
							if w:
								print('┘', end='') # N,W
							else:
								print('│', end='') # N
				elif e:
					if s:
						if w:
							print('┬', end='') # E,S,W
						else:
							print('┌', end='') # E,S
					else:
						if w:
							print('─', end='') # E,W
						else:
							print('─', end='') # E

				elif s:
					if w:
						print('┐', end='') # S,W
					else:
						print('│', end='') # S

				elif w:
					print('─', end='') # W

				else:
					print(' ', end='') # Unexplored/Nonexistent
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
			print(roomChars[y][x] if (x, y) not in printRoom.items else printRoom.items[(x, y)].render(detected), end='')
		print(floor if printRoom.neighbours[1] is not None and (y > const.ROOM_HEIGHT / 2 - 1 and not exitPrinted) else wall)
		if y > const.ROOM_HEIGHT / 2 - 1:
			exitPrinted = True

	for x in range(math.ceil(const.ROOM_WIDTH / 2)):
		print(wall, end='')
	print(floor if printRoom.neighbours[2] is not None else wall, end='')
	for x in range(math.ceil(const.ROOM_WIDTH / 2)):
		print(wall, end='')

	print(blankf)

def items(itemList: List[str]):
	print("Items: ", end='')
	for item in itemList:
		print(item, end='\n       ') # End is to line up list

	print()

def highscores(scores):
	header()
	print('Highscores')
	for score in scores: print(score)
	input('Press enter to continue.')

def thankyou():
	header()
	print('Thanks for playing!')
	print()