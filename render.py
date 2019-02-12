from typing import List

import math
import constants as const
import subprocess

def welcome():
	header()
	print('Welcome to charmed.')
	print('Ensure your terminal window is full-screen')
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
	print('\x1b[0;97;40mMovement: \x1b[48;5;21mh\x1b[0;97;40m \x1b[38;5;0m\x1b[48;5;226ml\x1b[0;97;40m')
	print('          \x1b[48;5;29mb\x1b[38;5;0m\x1b[48;5;46mj\x1b[48;5;154mn\x1b[0;97;40m')
	print()
	print('          \x1b[48;5;91my\x1b[48;5;208mu\x1b[0;97;40m')
	print('          \x1b[48;5;21mh\x1b[38;5;0m\x1b[48;5;46mj\x1b[38;5;15m\x1b[48;5;196mk\x1b[38;5;0m\x1b[48;5;226ml\x1b[0;97;40m')
	print('          \x1b[48;5;29mb\x1b[38;5;0m\x1b[48;5;154mn')
	print('\x1b[0;97;40m')
	print('Press "?" at any time for help.')
	print('Commands on startup text: "\'" to skip tutorial')
	print('                          "d" to set difficulty')
	print('                          "s" to set seed')
	print()
	input('Press enter to continue.')

def header():
	subprocess.call('clear')
	print('\x1b[0;97;40m', end='')
	print('=============== Charmed ===============')

def stats(health, armour, attack):
	print('Health: ', end='')
	print('♥' * int(max(health / 10, 1)))

	print('Armour: ', end='')
	print('✚' * int(max(armour / 10, 1)))

	print('Attack: ', end='')
	print('♠︎' * int(max(attack / 10, 1)))

def rooms(roomMap: List[List[int]]):
	"""
	The list is a list of bytes where each bit is significant.
	Byte: leudnesw
	l: Whether the tile contains the player
	e: Whether the tile contains the dungeon's exit
	u: Whether the tile contains an upward staircase
	d: Whether the tile contains a downward staircase
	n: Whether the tile has a northern exit
	e: Whether the tile has an eastern exit
	s: Whether the tile has a southern exit
	W: Whether the tile has a western exit

	To show an unexplored room, set all bits to 0
	"""
	print('\x1b[38;5;15m\x1b[48;5;215m' + ('#' * (const.MAP_WIDTH + 1)))

	for y in roomMap:
		print('\x1b[38;5;15m\x1b[48;5;215m#', end='')
		for c in y:
			if c & 0b10000000:
				print('\x1b[0;33;103m@', end='')
			elif c & 0b01000000:
				print('\x1b[0;35;105m⌘', end='')
			elif c & 0b00100000:
				print('\x1b[0;33;103m<', end='')
			elif c & 0b00010000:
				print('\x1b[0;33;103m>', end='')
			else:
				n = c & 0b00001000 == 8
				e = c & 0b00000100 == 4
				s = c & 0b00000010 == 2
				w = c & 0b00000001 == 1
				if n:
					if e:
						if s:
							if w:
								print('╋', end='') # N,E,S,W
							else:
								print('┣', end='') # N,E,S
						else:
							if w:
								print('┻', end='') # N,E,W
							else:
								print('┗', end='') # N,E
					else:
						if s:
							if w:
								print('┫', end='') # N,S,W
							else:
								print('|', end='') # N,S
						else:
							if w:
								print('┛', end='') # N,W
							else:
								print('↑', end='') # N
				elif e:
					if s:
						if w:
							print('┳', end='') # E,S,W
						else:
							print('┏', end='') # E,S
					else:
						if w:
							print('–', end='') # E,W
						else:
							print('→', end='') # E

				elif s:
					if w:
						print('┓', end='') # S,W
					else:
						print('↓', end='') # S

				elif w:
					print('←', end='') # W

				else:
					print(' ', end='')
		print('\x1b[38;5;15m\x1b[48;5;215m#')

	print('\x1b[38;5;15m\x1b[48;5;215m' + ('#' * (const.MAP_WIDTH + 2)) + '\x1b[0;97;40m')

def room(roomChars: List[List[str]]):
	for x in range(math.ceil(const.ROOM_WIDTH / 2)):
		print('\x1b[38;5;15m\x1b[48;5;215m#', end='')
	print('\x1b[0;97;40m.', end='')
	for x in range(math.ceil(const.ROOM_WIDTH / 2)):
		print('\x1b[38;5;15m\x1b[48;5;215m#', end='')
	print()

	exitPrinted = False

	for y in range(len(roomChars)):
		print('\x1b[0;97;40m.' if y > const.ROOM_HEIGHT / 2 and not exitPrinted else '\x1b[38;5;15m\x1b[48;5;215m#', end='')
		for x in range(len(roomChars[y])):
			print(roomChars[y][x], end='')
		print('\x1b[0;97;40m.' if y > const.ROOM_HEIGHT / 2 and not exitPrinted else '\x1b[38;5;15m\x1b[48;5;215m#')
		if y > const.ROOM_HEIGHT / 2:
			exitPrinted = True

	for x in range(math.ceil(const.ROOM_WIDTH / 2)):
		print('\x1b[38;5;15m\x1b[48;5;215m#', end='')
	print('\x1b[0;97;40m.', end='')
	for x in range(math.ceil(const.ROOM_WIDTH / 2)):
		print('\x1b[38;5;15m\x1b[48;5;215m#', end='')

def items(itemList: List[str]):
	print("Items: ", end='')
	for item in itemList:
		print(item, end='\n       ') # End is to line up list

	print()
