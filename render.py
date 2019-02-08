from typing import List

import math
import constants as const
import subprocess

def welcome():
	header()
	print('Welcome to charmed.')
	print('Ensure your terminal window is full-screen')
	return input('Press enter to continue. ') == 'k'

def difficulty():
	header()
	print('Difficulty: [1] Easy (Monsters have less health and attack, and helpful items spawn more frequently')
	print('            [2] Normal (Recommended)')
	print('            [3] Hard (Monsters have more health and attack, and harmful items spawn more frequently)')
	print("            [4] Insane (Monsters have more health and attack, and helpful items don't spawn")
	return input('Input a value: ')

def seed():
	header()
	return input('Seed (leave blank for random): ')

def generating():
	header()
	print('Generating. Please wait.')

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
	print('\x1b[38;5;15m\x1b[48;5;215m' + ('#' * (const.MAP_WIDTH + 2)))

	for y in roomMap:
		for c in y:
			if c & 0b10000000:
				print('\x1b[0;33;103m@')
			elif c & 0b01000000:
				print('\x1b[0;35;105m⌘')
			elif c & 0b00100000:
				print('\x1b[0;33;103m<')
			elif c & 0b00010000:
				print('\x1b[0;33;103m>')
			else:
				n = c & 0b00001000 == 8
				e = c & 0b00000100 == 4
				s = c & 0b00000010 == 2
				w = c & 0b00000001 == 1
				if n:
					if e:
						if s:
							if w:
								print('╋') # N,E,S,W
							else:
								print('┣') # N,E,S
						else:
							if w:
								print('┻') # N,E,W
							else:
								print('┗') # N,E
					else:
						if s:
							if w:
								print('┫') # N,S,W
							else:
								print('|') # N,S
						else:
							if w:
								print('┛') # N,W
							else:
								print('↑') # N
				elif e:
					if s:
						if w:
							print('┳') # E,S,W
						else:
							print('┏') # E,S
					else:
						if w:
							print('–') # E,W
						else:
							print('→') # E

				elif s:
					if w:
						print('┓') # S,W
					else:
						print('↓') # S

				elif w:
					print('←') # W

				else:
					print(' ')

	print('\x1b[38;5;15m\x1b[48;5;215m' + ('#' * (const.MAP_WIDTH + 2)))


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
