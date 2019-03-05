from room import *
from item import definitions as items
from monster import definitions as monsters
from typing import List, Any
from subprocess import Popen
from pynput import keyboard

import math
import room as roomDef
import os
import fileio as io
import random as randLib
import render as rd
import constants as const
import room


def rand(rMin, rMax) -> int:
	return randLib.randint(rMin, rMax)


def log(*values):
	if const.DEBUG:
		print(*values)


def generateMap(difficulty, seed=randLib.seed):
	randLib.seed(seed)

	generatedMap: List[List[Any]] = []

	for depth in range(const.MAX_DEPTH):
		currentMap: List[List[Any]] = []

		log('Depth', depth)
		# Generate the indices for this depth
		for row in range(const.MAP_HEIGHT):
			currentMap.append([])
			for currentRoom in range(const.MAP_WIDTH):
				currentMap[row].append(None)

		log('Path')
		# 1 = N, 2 = E, 3 = S, 4 = W
		beginSide = rand(1, 4) if depth is not 0 else 3
		endSide = (beginSide + 1) % 4 + 1

		roomsToRandomise: List[Room] = []

		if beginSide % 2 is 0:
			beginLoc = (0 if beginSide is 4 else const.MAP_WIDTH - 1, rand(0, const.MAP_HEIGHT - 1))
			endLoc = (0 if endSide is 4 else const.MAP_WIDTH - 1, rand(0, const.MAP_HEIGHT - 1))

			currentMap[beginLoc[1]][beginLoc[0]] = Room(beginLoc[0], beginLoc[1], bodies.EXIT if depth is 0 else bodies.UPSTAIR)
			if depth is const.MAX_DEPTH - 1:
				charmRoom = Room(endLoc[0], endLoc[1], bodies.CHARM)
				charmRoom.items[(int(const.ROOM_WIDTH / 2), int(const.ROOM_HEIGHT / 2))] = items.Charm(room, int(const.ROOM_WIDTH / 2), int(const.ROOM_HEIGHT / 2))
				currentMap[endLoc[1]][endLoc[0]] = charmRoom
			else:
				currentMap[endLoc[1]][endLoc[0]] = Room(endLoc[0], endLoc[1], bodies.DOWNSTAIR)

			currentMap.append([beginLoc, endLoc])

			currentLoc: List[int] = [beginLoc[0], beginLoc[1]] if beginSide is 4 else [endLoc[0], endLoc[1]]
			finLoc = [endLoc[0], endLoc[1]] if endSide is 2 else [beginLoc[0], beginLoc[1]]

			finRoom: Room = currentMap[finLoc[1]][finLoc[0]]

			log(currentLoc)
			log(finLoc)

			lastRoom = currentMap[currentLoc[1]][currentLoc[0]]
			lastRoomDir = 2

			roomsToRandomise.append(lastRoom)

			while not (currentLoc[0] == finLoc[0] and currentLoc[1] == finLoc[1]):
				if currentLoc[0] is const.MAP_WIDTH - 1:  # If on the opposite edge
					possibleDirs = [3 if currentLoc[1] < finLoc[1] else 1]  # Move up or down only depending on where we are in relation to the exit
				elif lastRoomDir is 2:
					possibleDirs = [2, 3] if currentLoc[1] is 0 else ([1, 2] if currentLoc[1] is const.MAP_HEIGHT - 1 else [1, 2, 3])  # Move up, down or right randomly according to the bounds of the map
				elif lastRoomDir is 3:
					possibleDirs = [2] if currentLoc[1] is const.MAP_HEIGHT - 1 else [2, 3]
				elif lastRoomDir is 1:
					possibleDirs = [2] if currentLoc[1] is 0 else [1, 2]
				else:
					raise IndexError('Unexpected map generation error')

				newDir = randLib.choice(possibleDirs)
				if newDir is 1:
					currentLoc[1] -= 1
				elif newDir is 2:
					currentLoc[0] += 1
				elif newDir is 3:
					currentLoc[1] += 1
				else:
					raise IndexError('Unexpected map generation error')

				log(currentLoc)

				if not (currentLoc[0] == finLoc[0] and currentLoc[1] == finLoc[1]):
					newRoom = Room(currentLoc[0], currentLoc[1], definitions.PATH)
					currentMap[currentLoc[1]][currentLoc[0]] = newRoom
					lastRoom.neighbours[newDir - 1] = newRoom
					newRoom.neighbours[(newDir + 2) % 4 - 1] = lastRoom

					lastRoom = newRoom
					lastRoomDir = newDir

					roomsToRandomise.append(newRoom)
				else:
					lastRoom.neighbours[newDir - 1] = finRoom
					finRoom.neighbours[(newDir + 2) % 4 - 1] = lastRoom

					roomsToRandomise.append(finRoom)
		else:
			beginLoc = (rand(0, const.MAP_WIDTH - 1), 0 if beginSide is 1 else const.MAP_HEIGHT - 1)
			endLoc = (rand(0, const.MAP_WIDTH - 1), 0 if endSide is 1 else const.MAP_HEIGHT - 1)

			currentMap[beginLoc[1]][beginLoc[0]] = Room(beginLoc[0], beginLoc[1], bodies.EXIT if depth is 0 else bodies.UPSTAIR)
			if depth is const.MAX_DEPTH - 1:
				charmRoom = Room(endLoc[0], endLoc[1], bodies.CHARM)
				charmRoom.items[(int(const.ROOM_WIDTH / 2), int(const.ROOM_HEIGHT / 2))] = items.Charm(room, int(const.ROOM_WIDTH / 2), int(const.ROOM_HEIGHT / 2))
				currentMap[endLoc[1]][endLoc[0]] = charmRoom
			else:
				currentMap[endLoc[1]][endLoc[0]] = Room(endLoc[0], endLoc[1], bodies.DOWNSTAIR)

			currentMap.append([beginLoc, endLoc])

			currentLoc = [beginLoc[0], beginLoc[1]] if beginSide is 1 else [endLoc[0], endLoc[1]]
			finLoc = [endLoc[0], endLoc[1]] if endSide is 3 else [beginLoc[0], beginLoc[1]]

			finRoom: Room = currentMap[finLoc[1]][finLoc[0]]

			log(currentLoc)
			log(finLoc)

			lastRoom = currentMap[currentLoc[1]][currentLoc[0]]
			lastRoomDir = 3

			roomsToRandomise.append(lastRoom)

			while not (currentLoc[0] == finLoc[0] and currentLoc[1] == finLoc[1]):
				if currentLoc[1] is const.MAP_HEIGHT - 1:  # If on the opposite edge
					possibleDirs = [4 if currentLoc[0] > finLoc[0] else 2]  # Move left or right only depending on where we are in relation to the exit
				elif lastRoomDir is 3:
					possibleDirs = [2, 3] if currentLoc[0] is 0 else ([3, 4] if currentLoc[0] is const.MAP_WIDTH - 1 else [2, 3, 4])  # Move left, down or right randomly according to the bounds of the map
				elif lastRoomDir is 2:
					possibleDirs = [3] if currentLoc[0] is const.MAP_WIDTH - 1 else [2, 3]
				elif lastRoomDir is 4:
					possibleDirs = [3] if currentLoc[0] is 0 else [3, 4]
				else:
					raise IndexError('Unexpected map generation error')

				newDir = randLib.choice(possibleDirs)
				if newDir is 2:
					currentLoc[0] += 1
				elif newDir is 3:
					currentLoc[1] += 1
				elif newDir is 4:
					currentLoc[0] -= 1
				else:
					raise IndexError('Unexpected map generation error')

				log(currentLoc)

				if not (currentLoc[0] == finLoc[0] and currentLoc[1] == finLoc[1]):
					newRoom = Room(currentLoc[0], currentLoc[1], definitions.PATH)
					currentMap[currentLoc[1]][currentLoc[0]] = newRoom
					lastRoom.neighbours[newDir - 1] = newRoom
					newRoom.neighbours[(newDir + 2) % 4 - 1] = lastRoom

					lastRoom = newRoom
					lastRoomDir = newDir

					roomsToRandomise.append(newRoom)
				else:
					lastRoom.neighbours[newDir - 1] = finRoom
					finRoom.neighbours[(newDir + 2) % 4 - 1] = lastRoom

					roomsToRandomise.append(finRoom)

		log('Branches')
		while len(roomsToRandomise) is not 0:
			currentRoom = roomsToRandomise[0]
			for i in range(1, 5):
				if currentRoom.neighbours[i - 1] is not None: continue

				newRoom: Room = None
				if i is 1 and currentRoom.y is not 0 and currentMap[currentRoom.y - 1][currentRoom.x] is None and rand(0, 100) < 50:
					newRoom = Room(currentRoom.x, currentRoom.y - 1, bodies.GENERIC)
					currentMap[currentRoom.y - 1][currentRoom.x] = newRoom

				if i is 2 and currentRoom.x is not const.MAP_WIDTH - 1 and currentMap[currentRoom.y][currentRoom.x + 1] is None and rand(0, 100) < 50:
					newRoom = Room(currentRoom.x + 1, currentRoom.y, bodies.GENERIC)
					currentMap[currentRoom.y][currentRoom.x + 1] = newRoom

				if i is 3 and currentRoom.y is not const.MAP_HEIGHT - 1 and currentMap[currentRoom.y + 1][currentRoom.x] is None and rand(0, 100) < 50:
					newRoom = Room(currentRoom.x, currentRoom.y + 1, bodies.GENERIC)
					currentMap[currentRoom.y + 1][currentRoom.x] = newRoom

				if i is 4 and currentRoom.x is not 0 and currentMap[currentRoom.y][currentRoom.x - 1] is None and rand(0, 100) < 50:
					newRoom = Room(currentRoom.x - 1, currentRoom.y, bodies.GENERIC)
					currentMap[currentRoom.y][currentRoom.x - 1] = newRoom

				if newRoom is not None:
					currentRoom.neighbours[i - 1] = newRoom
					newRoom.neighbours[(i + 1) % 4] = currentRoom
					roomsToRandomise.append(newRoom)
					log('[' + str(newRoom.x) + ', ' + str(newRoom.y) + ']')
			roomsToRandomise.remove(currentRoom)

		generatedMap.append(currentMap)

		log('Items')
		for y in range(len(currentMap) - 1):
			for currentRoom in currentMap[y]:
				if currentRoom is not None:
					numitems = max(rand(-5, 2), 0)
					for i in range(numitems):
						item = random.choice(items.possibleItems[difficulty - 1][depth])

						x, y = rand(0, const.ROOM_WIDTH - 1), rand(0, const.ROOM_HEIGHT - 1)
						while (x, y) in currentRoom.items or currentRoom.body[y][x] in room.BLOCKING:
							x, y = rand(0, const.ROOM_WIDTH - 1), rand(0, const.ROOM_HEIGHT - 1)

						if item is 0:
							currentRoom.items[(x, y)] = items.Gold(currentRoom, x, y)
						if item is 1:
							currentRoom.items[(x, y)] = items.Chance(currentRoom, x, y, depth, difficulty)
						if item is 2:
							currentRoom.items[(x, y)] = items.Detector(currentRoom, x, y)
						if item is 3:
							currentRoom.items[(x, y)] = items.Boost(currentRoom, x, y, depth)
						if item is 4:
							currentRoom.items[(x, y)] = items.MonsterTrap(currentRoom, x, y)

	return generatedMap


def roomToInt(room: Room, explored, detected: bool) -> int:
	if room is None: return 0

	i = 0
	if detected and len(room.items) > 0:
		i |= 0b10000000
	if explored:
		if room.exit is not None:
			i |= 0b01000000
		if room.upstair is not None:
			i |= 0b00100000
		if room.downstair is not None:
			i |= 0b00010000
		if room.neighbours[0] is not None:
			i |= 0b00001000
		if room.neighbours[1] is not None:
			i |= 0b00000100
		if room.neighbours[2] is not None:
			i |= 0b00000010
		if room.neighbours[3] is not None:
			i |= 0b00000001

	return i


command = ''
keyPressed = False


def keyPress(key):
	global command, keyPressed
	if type(key) is keyboard.KeyCode and keyPressed is False:
		command = str(key.char)
		keyPressed = True


def generateMonsters(rooms, depth, difficulty):
	generated = []
	for currentRoom in rooms:
		nummonsters = max(rand(-3, 2), 0)
		for i in range(nummonsters):
			monster = random.choice(monsters.possibleMonsters[depth + difficulty - 1])

			x, y = rand(0, const.ROOM_WIDTH - 1), rand(0, const.ROOM_HEIGHT - 1)
			while currentRoom.body[y][x] in room.BLOCKING:
				x, y = rand(0, const.ROOM_WIDTH - 1), rand(0, const.ROOM_HEIGHT - 1)

			if monster is 0:
				new = monsters.Beetle(x, y, currentRoom, difficulty)
			elif monster is 1:
				new = monsters.Scorpion(x, y, currentRoom, difficulty)
			elif monster is 2:
				new = monsters.Mummy(x, y, currentRoom, difficulty)
			elif monster is 3:
				new = monsters.Slave(x, y, currentRoom, difficulty)
			elif monster is 4:
				new = monsters.Pharaoh(x, y, currentRoom, difficulty)
			elif monster is 5:
				new = monsters.Lek(x, y, currentRoom, difficulty)
			elif monster is 6:
				new = monsters.Chin(x, y, currentRoom, difficulty)
			new.room.monsters[(x, y)] = new
			generated.append(new)
	return generated


def playGame(gameMap, difficulty, seed):
	dhealth = 0
	darmour = 0
	dattack = 0
	dscore = 0

	health = const.START_HEALTH
	armour = const.START_ARMOUR
	attack = const.START_ATTACK
	score = 0
	charm = False
	died = False
	explored = []

	global command, keyPressed

	# Generate explored map
	for d in range(len(gameMap)):
		explored.append([])
		for y in range(len(gameMap[d])):
			explored[d].append([])
			for x in range(len(gameMap[d][y])):
				explored[d][y].append(const.DEBUG)

	track: Popen = None
	filePath = os.path.dirname(os.path.realpath(__file__))

	depth = 0
	itemsDetected = False

	currentDepth: List[List[Room]] = gameMap[depth]
	currentDepthRooms = []
	for y in range(len(currentDepth) - 1):
		for eachRoom in currentDepth[y]:
			if eachRoom is not None:
				currentDepthRooms.append(eachRoom)

	posRooms: List[int] = list(currentDepth[len(currentDepth) - 1][0])
	currentRoom: Room = currentDepth[posRooms[1]][posRooms[0]]
	posInt: List[int] = list(currentRoom.entryPoint)

	loadedMonsters = generateMonsters(currentDepthRooms, depth, difficulty)

	noclip = False
	newInfo = ''
	explored[depth][posRooms[1]][posRooms[0]] = True

	keyListener = keyboard.Listener(on_press=keyPress)
	keyListener.start()

	# Main loop
	while True:
		rd.header()
		rd.stats(health, dhealth, attack, dattack, armour, darmour, score, dscore, charm)
		dhealth, darmour, dattack, dscore = 0, 0, 0, 0

		rd.rooms([
			[roomToInt(currentDepth[y][x], explored[depth][y][x], itemsDetected and currentDepth[y][x].items.values() is not None)
			 if currentDepth[y][x] is not None else 0
			 for x in range(len(currentDepth[y]))]
			for y in range(len(currentDepth) - 1)
		], posRooms)

		print()

		rd.room(currentRoom, itemsDetected, posInt)

		if health <= 0:
			print('You died...')
			input('Press enter to continue.')
			rd.highscores(io.getHighScores())
			return

		if newInfo != '':
			print(newInfo)
			newInfo = ''

		keyPressed = False
		while keyPressed is False:
			continue

		if command == '>':
			input('')
			command = input('Enter command: ')

		didMove = False
		log('Command: "' + command + '"')

		# Megalovania: TODO: Remove from GJ Version
		if command == 'megalovania':
			if track is not None:
				track.terminate()

			track = Popen(['/usr/bin/afplay', filePath + '/data/music (hidden).mp3'])

		# Cheat codes
		elif command == 'winxp':  # (Windows) eXPlore
			for d in range(len(explored)):
				for y in range(len(explored[d])):
					for x in range(len(explored[d][y])):
						explored[d][y][x] = True
		elif command == 'kkjjhlhlba':  # Konami code, must have
			charm = True
		elif command == 'northernlights':  # "May I see it?"
			itemsDetected = True
		elif command == 'noclip':  # Stop monsters moving
			noclip = not noclip
		elif command == 'deadlylazer': # The sun is a deadly lazer
			for monster in loadedMonsters:
				monster.room.monsters[(monster.x, monster.y)] = None
				loadedMonsters.remove(monster)

		# Movement - Cardinal
		elif command == 'h' or command == 'a':
			if posInt[0] > 0:
				if currentRoom.monsters[(posInt[0] - 1, posInt[1])] is not None:
					newInfo = currentRoom.monsters[(posInt[0] - 1, posInt[1])].hitmsg()
					if currentRoom.monsters[(posInt[0] - 1, posInt[1])].hit(attack):
						loadedMonsters.remove(currentRoom.monsters[(posInt[0] - 1, posInt[1])])
						currentRoom.monsters[(posInt[0] - 1, posInt[1])] = None
					didMove = True
				elif currentRoom.body[posInt[1]][posInt[0] - 1] not in roomDef.BLOCKING:
					posInt[0] -= 1
					didMove = True
				elif charm and currentRoom.body[posInt[1]][posInt[0] - 2] not in roomDef.BLOCKING:
					posInt[0] -= 2
					didMove = True
				else:
					newInfo = 'You can\'t move that way.'
			elif posInt[1] == int(const.ROOM_HEIGHT / 2) and currentRoom.neighbours[3] is not None:
				posInt[0] = const.ROOM_WIDTH - 1
				posRooms[0] -= 1
				didMove = True
		elif command == 'j' or command == 's':
			if posInt[1] < const.ROOM_HEIGHT - 1:
				if currentRoom.monsters[(posInt[0], posInt[1] + 1)] is not None:
					newInfo = currentRoom.monsters[(posInt[0], posInt[1] + 1)].hitmsg()
					if currentRoom.monsters[(posInt[0], posInt[1] + 1)].hit(attack):
						loadedMonsters.remove(currentRoom.monsters[(posInt[0], posInt[1] + 1)])
						currentRoom.monsters[(posInt[0], posInt[1] + 1)] = None
					didMove = True
				elif currentRoom.body[posInt[1] + 1][posInt[0]] not in roomDef.BLOCKING:
					posInt[1] += 1
					didMove = True
				elif charm and currentRoom.body[posInt[1] + 2][posInt[0]] not in roomDef.BLOCKING:
					posInt[1] += 2
					didMove = True
				else:
					newInfo = 'You can\'t move that way.'
			elif posInt[0] == int(const.ROOM_WIDTH / 2) and currentRoom.neighbours[2] is not None:
				posInt[1] = 0
				posRooms[1] += 1
				didMove = True
		elif command == 'k' or command == 'w':
			if posInt[1] > 0:
				if currentRoom.monsters[(posInt[0], posInt[1] - 1)] is not None:
					newInfo = currentRoom.monsters[(posInt[0], posInt[1] - 1)].hitmsg()
					if currentRoom.monsters[(posInt[0], posInt[1] - 1)].hit(attack):
						loadedMonsters.remove(currentRoom.monsters[(posInt[0], posInt[1] - 1)])
						currentRoom.monsters[(posInt[0], posInt[1] - 1)] = None
					didMove = True
				elif currentRoom.body[posInt[1] - 1][posInt[0]] not in roomDef.BLOCKING:
					posInt[1] -= 1
					didMove = True
				elif charm and currentRoom.body[posInt[1] - 2][posInt[0]] not in roomDef.BLOCKING:
					posInt[1] -= 2
					didMove = True
				else:
					newInfo = 'You can\'t move that way.'
			elif posInt[0] == int(const.ROOM_WIDTH / 2) and currentRoom.neighbours[0] is not None:
				posInt[1] = const.ROOM_HEIGHT - 1
				posRooms[1] -= 1
				didMove = True
		elif command == 'l' or command == 'd':
			if posInt[0] < const.ROOM_WIDTH - 1:
				if currentRoom.monsters[(posInt[0] + 1, posInt[1])] is not None:
					newInfo = currentRoom.monsters[(posInt[0] + 1, posInt[1])].hitmsg()
					if currentRoom.monsters[(posInt[0] + 1, posInt[1])].hit(attack):
						loadedMonsters.remove(currentRoom.monsters[(posInt[0] + 1, posInt[1])])
						currentRoom.monsters[(posInt[0] + 1, posInt[1])] = None
					didMove = True
				elif currentRoom.body[posInt[1]][posInt[0] + 1] not in roomDef.BLOCKING:
					posInt[0] += 1
					didMove = True
				elif charm and currentRoom.body[posInt[1]][posInt[0] + 2] not in roomDef.BLOCKING:
					posInt[0] += 2
					didMove = True
				else:
					newInfo = 'You can\'t move that way.'
			elif posInt[1] == int(const.ROOM_HEIGHT / 2) and currentRoom.neighbours[1] is not None:
				posInt[0] = 0
				posRooms[0] += 1
				didMove = True
		# Diagonal
		elif command == 'y':
			if posInt[0] > 0 and posInt[1] > 0:
				if currentRoom.monsters[(posInt[0] - 1, posInt[1] - 1)] is not None:
					newInfo = currentRoom.monsters[(posInt[0] - 1, posInt[1] - 1)].hitmsg()
					if currentRoom.monsters[(posInt[0] - 1, posInt[1] - 1)].hit(attack):
						loadedMonsters.remove(currentRoom.monsters[(posInt[0] - 1, posInt[1] - 1)])
						currentRoom.monsters[(posInt[0] - 1, posInt[1] - 1)] = None
					didMove = True
				elif currentRoom.body[posInt[1] - 1][posInt[0] - 1] not in roomDef.BLOCKING and (charm or (currentRoom.body[posInt[1] - 1][posInt[0]] not in roomDef.BLOCKING and currentRoom.body[posInt[1]][posInt[0] - 1] not in roomDef.BLOCKING)):
					posInt[0] -= 1
					posInt[1] -= 1
					didMove = True
				elif charm and currentRoom.body[posInt[1] - 2][posInt[0] - 2] not in roomDef.BLOCKING:
					posInt[0] -= 2
					posInt[1] -= 2
					didMove = True
				else:
					newInfo = 'You can\'t move that way.'
		elif command == 'u':
			if posInt[0] < const.ROOM_WIDTH - 1 and posInt[1] > 0:
				if currentRoom.monsters[(posInt[0] + 1, posInt[1] - 1)] is not None:
					newInfo = currentRoom.monsters[(posInt[0] + 1, posInt[1] - 1)].hitmsg()
					if currentRoom.monsters[(posInt[0] + 1, posInt[1] - 1)].hit(attack):
						loadedMonsters.remove(currentRoom.monsters[(posInt[0] + 1, posInt[1] - 1)])
						currentRoom.monsters[(posInt[0] + 1, posInt[1] - 1)] = None
					didMove = True
				elif currentRoom.body[posInt[1] - 1][posInt[0] + 1] not in roomDef.BLOCKING and (charm or (currentRoom.body[posInt[1] - 1][posInt[0]] not in roomDef.BLOCKING and currentRoom.body[posInt[1]][posInt[0] + 1] not in roomDef.BLOCKING)):
					posInt[0] += 1
					posInt[1] -= 1
					didMove = True
				elif charm and currentRoom.body[posInt[1] - 2][posInt[0] + 2] not in roomDef.BLOCKING:
					posInt[0] += 2
					posInt[1] -= 2
					didMove = True
				else:
					newInfo = 'You can\'t move that way.'
		elif command == 'b':
			if posInt[0] > 0 and posInt[1] < const.ROOM_HEIGHT - 1:
				if currentRoom.monsters[(posInt[0] - 1, posInt[1] + 1)] is not None:
					newInfo = currentRoom.monsters[(posInt[0] - 1, posInt[1] + 1)].hitmsg()
					if currentRoom.monsters[(posInt[0] - 1, posInt[1] + 1)].hit(attack):
						loadedMonsters.remove(currentRoom.monsters[(posInt[0] - 1, posInt[1] + 1)])
						currentRoom.monsters[(posInt[0] - 1, posInt[1] + 1)] = None
					didMove = True
				elif currentRoom.body[posInt[1] + 1][posInt[0] - 1] not in roomDef.BLOCKING and (charm or (currentRoom.body[posInt[1] + 1][posInt[0]] not in roomDef.BLOCKING and currentRoom.body[posInt[1]][posInt[0] - 1] not in roomDef.BLOCKING)):
					posInt[0] -= 1
					posInt[1] += 1
					didMove = True
				elif charm and currentRoom.body[posInt[1] + 2][posInt[0] - 2] not in roomDef.BLOCKING:
					posInt[0] -= 2
					posInt[1] += 2
					didMove = True
				else:
					newInfo = 'You can\'t move that way.'
		elif command == 'n':
			if posInt[0] < const.ROOM_WIDTH - 1 and posInt[1] < const.ROOM_HEIGHT - 1:
				if currentRoom.monsters[(posInt[0] + 1, posInt[1] + 1)] is not None:
					newInfo = currentRoom.monsters[(posInt[0] + 1, posInt[1] + 1)].hitmsg()
					if currentRoom.monsters[(posInt[0] + 1, posInt[1] + 1)].hit(attack):
						loadedMonsters.remove(currentRoom.monsters[(posInt[0] + 1, posInt[1] + 1)])
						currentRoom.monsters[(posInt[0] + 1, posInt[1] + 1)] = None
					didMove = True
				elif currentRoom.body[posInt[1] + 1][posInt[0] + 1] not in roomDef.BLOCKING and (charm or (currentRoom.body[posInt[1] + 1][posInt[0]] not in roomDef.BLOCKING and currentRoom.body[posInt[1]][posInt[0] + 1] not in roomDef.BLOCKING)):
					posInt[0] += 1
					posInt[1] += 1
					didMove = True
				elif charm and currentRoom.body[posInt[1] + 2][posInt[0] + 2] not in roomDef.BLOCKING:
					posInt[0] += 2
					posInt[1] += 2
					didMove = True
				else:
					newInfo = 'You can\'t move that way.'
		# Rest
		elif command == 'z':
			didMove = True

		# Quit and suspend
		elif command == 'q' or command == 'quit' and rd.reallyquit():
			if track is not None:
				track.terminate()
			keyListener.stop()
			io.putHighScore('Killed yourself', score)
			health = 0
		elif command == 'p':
			rd.suspend()

		# Seed and difficulty
		elif command == 'seed':
			newInfo = 'Seed: ' + seed
		elif command == 'diff' or command == 'difficulty':
			newInfo = 'Difficulty: ' + difficulty

		# Help
		elif command == '?':
			rd.commands()

		# Debug commands
		elif const.DEBUG:
			if command.startswith('d'):
				try:
					d = int(command[1:])
					if d <= const.MAX_DEPTH:
						depth = d
						currentDepth = gameMap[depth]
						posRooms = list(currentDepth[len(currentDepth) - 1][0])
						currentDepthRooms = []
						itemsDetected = False
						for y in range(len(currentDepth) - 1):
							for eachRoom in currentDepth[y]:
								if eachRoom is not None:
									currentDepthRooms.append(eachRoom)
						loadedMonsters = generateMonsters(currentDepthRooms, depth, difficulty)
				except Exception:
					pass

		if didMove:
			if currentDepth[posRooms[1]][posRooms[0]].downstair is not None and posInt[0] == currentDepth[posRooms[1]][posRooms[0]].downstair[0] and posInt[1] == currentDepth[posRooms[1]][posRooms[0]].downstair[1]:
				# Downstairs
				depth += 1
				currentDepth = gameMap[depth]
				currentDepthRooms = []
				itemsDetected = False
				for y in range(len(currentDepth) - 1):
					for eachRoom in currentDepth[y]:
						if eachRoom is not None:
							currentDepthRooms.append(eachRoom)
				loadedMonsters = generateMonsters(currentDepthRooms, depth, difficulty)

				posRooms = list(currentDepth[len(currentDepth) - 1][0])
				posInt = list(currentDepth[posRooms[1]][posRooms[0]].entryPoint)
			elif currentDepth[posRooms[1]][posRooms[0]].upstair is not None and posInt[0] == currentDepth[posRooms[1]][posRooms[0]].upstair[0] and posInt[1] == currentDepth[posRooms[1]][posRooms[0]].upstair[1]:
				# Upstairs
				depth -= 1
				currentDepth = gameMap[depth]
				currentDepthRooms = []
				itemsDetected = False
				for y in range(len(currentDepth) - 1):
					for eachRoom in currentDepth[y]:
						if eachRoom is not None:
							currentDepthRooms.append(eachRoom)
				loadedMonsters = generateMonsters(currentDepthRooms, depth, difficulty)

				posRooms = list(currentDepth[len(currentDepth) - 1][1])
				posInt = list(currentDepth[posRooms[1]][posRooms[0]].entryPoint)
			elif currentDepth[posRooms[1]][posRooms[0]].exit is not None and posInt[0] == currentDepth[posRooms[1]][posRooms[0]].exit[0] and posInt[1] == currentDepth[posRooms[1]][posRooms[0]].exit[1]:
				if charm:
					io.putHighScore('Left the dungeon', score)
					rd.highscores(io.getHighScores())
					return
				else:
					newInfo = "You can't teleport up to the helicopter without the Charm"

			explored[depth][posRooms[1]][posRooms[0]] = True  # Room is explored
			currentRoom = currentDepth[posRooms[1]][posRooms[0]]  # currentRoom is up to date

			if (posInt[0], posInt[1]) in currentRoom.items:
				modifiers = currentRoom.items[(posInt[0], posInt[1])].collect()
				dhealth = modifiers[0]
				health += modifiers[0]
				darmour = modifiers[1]
				armour += modifiers[1]
				dattack = modifiers[2]
				attack += modifiers[2]
				dscore = modifiers[3]
				score += modifiers[3]

				newInfo = modifiers[4]

				if modifiers[5] & 0b001 is not 0:
					itemsDetected = True
				if modifiers[5] & 0b010 is not 0:
					charm = True
				if modifiers[5] & 0b100 is not 0:
					for i in range(rand(2, 5)):
						monster = random.choice(monsters.possibleMonsters[depth + difficulty - 1])

						x, y = rand(0, const.ROOM_WIDTH - 1), rand(0, const.ROOM_HEIGHT - 1)
						while currentRoom.body[y][x] in room.BLOCKING:
							x, y = rand(0, const.ROOM_WIDTH - 1), rand(0, const.ROOM_HEIGHT - 1)

						if monster is 0:
							new = monsters.Beetle(x, y, currentRoom, difficulty)
						elif monster is 1:
							new = monsters.Scorpion(x, y, currentRoom, difficulty)
						elif monster is 2:
							new = monsters.Mummy(x, y, currentRoom, difficulty)
						elif monster is 3:
							new = monsters.Slave(x, y, currentRoom, difficulty)
						elif monster is 4:
							new = monsters.Pharaoh(x, y, currentRoom, difficulty)
						elif monster is 5:
							new = monsters.Lek(x, y, currentRoom, difficulty)
						elif monster is 6:
							new = monsters.Chin(x, y, currentRoom, difficulty)
						new.room.monsters[(x, y)] = new
						loadedMonsters.append(new)

				del currentRoom.items[(posInt[0], posInt[1])]

			# Monster movement
			if not noclip:
				for monster in loadedMonsters:
					monster.room.monsters[(monster.x, monster.y)] = None

					direction = monster.move(posRooms[0], posRooms[1], posInt[0], posInt[1])
					oldHealth = health
					if direction == 0:  # North
						if monster.y == 0:
							if currentDepth[monster.room.y - 1][monster.room.x].monsters[(monster.x, const.ROOM_HEIGHT - 1)] is None:
								monster.room = currentDepth[monster.room.y - 1][monster.room.x]
								monster.y = const.ROOM_HEIGHT - 1
							monster.target = randLib.choice([i for i in range(0, 4) if monster.room.neighbours[i] is not None])
						else:
							if monster.room.x == posRooms[0] and monster.room.y == posRooms[1] and monster.x == posInt[0] and monster.y - 1 == posInt[1]:
								health -= math.ceil(monster.attack() / armour)
								newInfo = ((newInfo + '; ') if newInfo != '' else '') + monster.attackmsg()
							else:
								monster.y -= 1
					elif direction == 1:  # North-East
						if monster.room.x == posRooms[0] and monster.room.y == posRooms[1] and monster.x + 1 == posInt[0] and monster.y - 1 == posInt[1]:
							health -= math.ceil(monster.attack() / armour)
							newInfo = ((newInfo + '; ') if newInfo != '' else '') + monster.attackmsg()
						else:
							monster.x += 1
							monster.y -= 1
					elif direction == 2:  # East
						if monster.x == const.ROOM_WIDTH - 1:
							if currentDepth[monster.room.y][monster.room.x + 1].monsters[(0, monster.y)] is None:
								monster.room = currentDepth[monster.room.y][monster.room.x + 1]
								monster.x = 0
							monster.target = randLib.choice([i for i in range(0, 4) if monster.room.neighbours[i] is not None])
						else:
							if monster.room.x == posRooms[0] and monster.room.y == posRooms[1] and monster.x + 1 == posInt[0] and monster.y == posInt[1]:
								health -= math.ceil(monster.attack() / armour)
								newInfo = ((newInfo + '; ') if newInfo != '' else '') + monster.attackmsg()
							else:
								monster.x += 1
					elif direction == 3:  # South-East
						if monster.room.x == posRooms[0] and monster.room.y == posRooms[1] and monster.x + 1 == posInt[0] and monster.y + 1 == posInt[1]:
							health -= math.ceil(monster.attack() / armour)
							newInfo = ((newInfo + '; ') if newInfo != '' else '') + monster.attackmsg()
						else:
							monster.x += 1
							monster.y += 1
					elif direction == 4:  # South
						if monster.y == const.ROOM_HEIGHT - 1:
							if currentDepth[monster.room.y + 1][monster.room.x].monsters[(monster.x, 0)] is None:
								monster.room = currentDepth[monster.room.y + 1][monster.room.x]
								monster.y = 0
							monster.target = randLib.choice([i for i in range(0, 4) if monster.room.neighbours[i] is not None])
						else:
							if monster.room.x == posRooms[0] and monster.room.y == posRooms[1] and monster.x == posInt[0] and monster.y + 1 == posInt[1]:
								health -= math.ceil(monster.attack() / armour)
								newInfo = ((newInfo + '; ') if newInfo != '' else '') + monster.attackmsg()
							else:
								monster.y += 1
					elif direction == 5:  # South-West
						if monster.room.x == posRooms[0] and monster.room.y == posRooms[1] and monster.x - 1 == posInt[0] and monster.y + 1 == posInt[1]:
							health -= math.ceil(monster.attack() / armour)
							newInfo = ((newInfo + '; ') if newInfo != '' else '') + monster.attackmsg()
						else:
							monster.x -= 1
							monster.y += 1
					elif direction == 6:  # West
						if monster.x == 0:
							if currentDepth[monster.room.y][monster.room.x - 1].monsters[(const.ROOM_WIDTH - 1, monster.y)] is None:
								monster.room = currentDepth[monster.room.y][monster.room.x - 1]
								monster.x = const.ROOM_WIDTH - 1
							monster.target = randLib.choice([i for i in range(0, 4) if monster.room.neighbours[i] is not None])
						else:
							if monster.room.x == posRooms[0] and monster.room.y == posRooms[1] and monster.x - 1 == posInt[0] and monster.y == posInt[1]:
								health -= math.ceil(monster.attack() / armour)
								newInfo = ((newInfo + '; ') if newInfo != '' else '') + monster.attackmsg()
							else:
								monster.x -= 1
					elif direction == 7:  # North-West
						if monster.room.x == posRooms[0] and monster.room.y == posRooms[1] and monster.x - 1 == posInt[0] and monster.y - 1 == posInt[1]:
							health -= math.ceil(monster.attack() / armour)
							newInfo = ((newInfo + '; ') if newInfo != '' else '') + monster.attackmsg()
						else:
							monster.x -= 1
							monster.y -= 1

					health = math.ceil(health)

					if health <= 0:
						io.putHighScore(monster.killedBy() + ' on depth ' + str(depth), score)
						died = True
						break
					dhealth = health - oldHealth

					monster.room.monsters[(monster.x, monster.y)] = monster

			if health <= 0 and not died:
				io.putHighScore('Killed by magic on depth ' + str(depth), score)

			armour = max(armour, 1)
			attack = max(attack, 1)

		if track is not None:
			if track.poll() is not None:
				track = None
			elif command == 'stop':
				track.terminate()
				track = None
