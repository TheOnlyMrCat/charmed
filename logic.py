from room import *
from objects.item import definitions as items
from typing import List, Any
from subprocess import Popen
from pynput import keyboard

import os
import fileio as io
import random as randLib
import render as rd
import constants as const

def rand(rMin, rMax) -> int:
	return randLib.randint(rMin, rMax)

def log(*values):
	if const.DEBUG:
		print(*values)

def generateMap(difficulty, seed = randLib.seed):
	randLib.seed(seed)

	generatedMap: List[List[Any]] = []

	for depth in range(const.MAX_DEPTH):
		currentMap: List[List[Any]] = []

		log('Depth', depth)
		# Generate the indices for this depth
		for row in range(const.MAP_HEIGHT):
			currentMap.append([])
			for room in range(const.MAP_WIDTH):
				currentMap[row].append(None)

		log('Path')
		# 1 = N, 2 = E, 3 = S, 4 = W
		beginSide = rand(1, 4) if depth is not 0 else 3
		endSide = (beginSide + 1) % 4 + 1

		roomsToRandomise: List[Room] = []

		if beginSide % 2 is 0:
			beginLoc = (0 if beginSide is 4 else const.MAP_WIDTH - 1, rand(0, const.MAP_HEIGHT - 1))
			endLoc   = (0 if endSide   is 4 else const.MAP_WIDTH - 1, rand(0, const.MAP_HEIGHT - 1))

			currentMap[beginLoc[1]][beginLoc[0]] = Room(beginLoc[0], beginLoc[1], bodies.EXIT if depth is 0 else bodies.UPSTAIR)
			currentMap[endLoc[1]][endLoc[0]] = Room(endLoc[0], endLoc[1], bodies.DOWNSTAIR if depth is not const.MAX_DEPTH else bodies.CHARM)

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
				if currentLoc[0] is const.MAP_WIDTH - 1: # If on the opposite edge
					possibleDirs = [3 if currentLoc[1] < finLoc[1] else 1] # Move up or down only depending on where we are in relation to the exit
				elif lastRoomDir is 2:
					possibleDirs = [2, 3] if currentLoc[1] is 0 else ([1, 2] if currentLoc[1] is const.MAP_HEIGHT - 1 else [1, 2, 3]) # Move up, down or right randomly according to the bounds of the map
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
			endLoc   = (rand(0, const.MAP_WIDTH - 1), 0 if endSide   is 1 else const.MAP_HEIGHT - 1)

			currentMap[beginLoc[1]][beginLoc[0]] = Room(beginLoc[0], beginLoc[1], bodies.EXIT if depth is 0 else bodies.UPSTAIR)
			currentMap[endLoc[1]][endLoc[0]] = Room(endLoc[0], endLoc[1], bodies.DOWNSTAIR if depth is not const.MAX_DEPTH else bodies.CHARM)

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
				if currentRoom.neighbours[i-1] is not None: continue

				newRoom: Room = None
				if i is 1 and currentRoom.y is not 0 and currentMap[currentRoom.y - 1][currentRoom.x] is None and rand(0, 100) < 50:
					newRoom = Room(currentRoom.x, currentRoom.y - 1, bodies.GENERIC)
					currentMap[currentRoom.y - 1][currentRoom.x] = newRoom

				if i is 2 and currentRoom.x is not const.MAP_WIDTH - 1 and currentMap[currentRoom.y][currentRoom.x + 1] is None and rand(0, 100) < 50:
					newRoom = Room(currentRoom.x + 1, currentRoom.y, bodies.GENERIC)
					currentMap[currentRoom.y][currentRoom.x + 1] = newRoom

				if i is 3 and currentRoom.y is not const.MAP_HEIGHT - 1 and currentMap[currentRoom.y + 1][currentRoom.x] is None and rand(0, 100) < 50:
					newRoom = Room(currentRoom.x, currentRoom.y + 1, bodies.GENERIC)
					currentMap[currentRoom.y + 1][currentRoom.x] = newRoom\

				if i is 4 and currentRoom.x is not 0 and currentMap[currentRoom.y][currentRoom.x - 1] is None and rand(0, 100) < 50:
					newRoom = Room(currentRoom.x - 1, currentRoom.y, bodies.GENERIC)
					currentMap[currentRoom.y][currentRoom.x - 1] = newRoom

				if newRoom is not None:
					currentRoom.neighbours[i-1] = newRoom
					newRoom.neighbours[(i+1)%4] = currentRoom
					roomsToRandomise.append(newRoom)
					log('[' + str(newRoom.x) + ', ' + str(newRoom.y) + ']')
			roomsToRandomise.remove(currentRoom)

		generatedMap.append(currentMap)

		log('Items')
		for y in range(len(currentMap)-1):
			for room in currentMap[y]:
				if room is not None:
					numitems = max(rand(-2, 2), 0)
					for i in range(numitems):
						item = random.choice(items.possibleItems[depth])

						x, y = rand(0, const.ROOM_WIDTH-1), rand(0, const.ROOM_HEIGHT-1)
						while room.body[y][x] == '#':
							x, y = rand(0, const.ROOM_WIDTH-1), rand(0, const.ROOM_HEIGHT-1)

						if item is 0:
							room.items[(x, y)] = items.Gold(room, x, y)
						if item is 1:
							room.items[(x, y)] = items.Chance(room, x, y)
						if item is 2:
							room.items[(x, y)] = items.Detector(room, x, y)
						if item is 3:
							room.items[(x, y)] = items.Boost(room, x, y, depth)

	return generatedMap

def roomToInt(room: Room, detected: bool) -> int:
	if room is None: return 0

	i = 0
	if detected:
		i |= 0b10000000
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

def playGame(gameMap):
	health = const.START_HEALTH
	armour = const.START_ARMOUR
	attack = const.START_ATTACK
	score = 0
	charm = False
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
	currentDepth: List[List[Room]] = gameMap[depth]
	posRooms: List[int] = list(currentDepth[len(currentDepth) - 1][0])
	currentRoom: Room = currentDepth[posRooms[1]][posRooms[0]]
	posInt: List[int] = list(currentRoom.entryPoint)

	explored[depth][posRooms[1]][posRooms[0]] = True

	keyListener = keyboard.Listener(on_press = keyPress)
	keyListener.start()

	# Main loop
	while True:
		rd.header()
		rd.stats(health, armour, attack, score, charm)

		rd.rooms([
			[roomToInt(currentDepth[y][x], False) if explored[depth][y][x] else 0 for x in range(len(currentDepth[y]))]
			for y in range(len(currentDepth) - 1)
		], posRooms)

		print()

		rd.room(currentRoom, False, posInt)

		keyPressed = False
		while keyPressed is False:
			continue

		if command == '>':
			input('')
			command = input('Enter command: ')

		didMove = False
		log('Command: "' + command + '"')

		# Megalovania
		if command == 'megalovania':
			if track is not None:
				track.terminate()

			track = Popen(['/usr/bin/afplay', filePath + '/data/music (hidden).mp3'])

		# Cheat codes
		elif command == 'winxp':
			for d in range(len(explored)):
				for y in range(len(explored[d])):
					for x in range(len(explored[d][y])):
						explored[d][y][x] = True
		elif command == 'kkjjhlhlba':
			charm = True

		# Movement - Cardinal
		elif command == 'h':
			if posInt[0] > 0:
				if currentRoom.body[posInt[1]][posInt[0] - 1] != '#':
					posInt[0] -= 1
					didMove = True
				elif charm and currentRoom.body[posInt[1]][posInt[0] - 2] != '#':
					posInt[0] -= 2
					didMove = True
			elif posInt[1] == int(const.ROOM_HEIGHT / 2) and currentRoom.neighbours[3] is not None:
				posInt[0] = const.ROOM_WIDTH - 1
				posRooms[0] -= 1
				didMove = True
		elif command == 'j':
			if posInt[1] < const.ROOM_HEIGHT - 1:
				if currentRoom.body[posInt[1] + 1][posInt[0]] != '#':
					posInt[1] += 1
					didMove = True
				elif charm and currentRoom.body[posInt[1] + 2][posInt[0]] != '#':
					posInt[1] += 2
					didMove = True
			elif posInt[0] == int(const.ROOM_WIDTH / 2) and currentRoom.neighbours[2] is not None:
				posInt[1] = 0
				posRooms[1] += 1
				didMove = True
		elif command == 'k':
			if posInt[1] > 0:
				if currentRoom.body[posInt[1] - 1][posInt[0]] != '#':
					posInt[1] -= 1
					didMove = True
				elif charm and currentRoom.body[posInt[1] - 2][posInt[0]] != '#':
					posInt[1] -= 2
					didMove = True
			elif posInt[0] == int(const.ROOM_WIDTH / 2) and currentRoom.neighbours[0] is not None:
				posInt[1] = const.ROOM_HEIGHT - 1
				posRooms[1] -= 1
				didMove = True
		elif command == 'l':
			if posInt[0] < const.ROOM_WIDTH - 1:
				if currentRoom.body[posInt[1]][posInt[0] + 1] != '#':
					posInt[0] += 1
					didMove = True
				elif charm and currentRoom.body[posInt[1]][posInt[0] + 2]:
					posInt[0] += 2
					didMove = True
			elif posInt[1] == int(const.ROOM_HEIGHT / 2) and currentRoom.neighbours[1] is not None:
				posInt[0] = 0
				posRooms[0] += 1
				didMove = True
		# Diagonal
		elif command == 'y':
			if posInt[0] > 0 and posInt[1] > 0:
				if currentRoom.body[posInt[1]-1][posInt[0]-1] != '#' and (charm or (currentRoom.body[posInt[1]-1][posInt[0]] != '#' and currentRoom.body[posInt[1]][posInt[0]-1] != '#')):
					posInt[0] -= 1
					posInt[1] -= 1
				elif charm and currentRoom.body[posInt[1]-2][posInt[0]-2] != '#':
					posInt[0] -= 2
					posInt[1] -= 2
		elif command == 'u':
			if posInt[0] < const.ROOM_WIDTH - 1 and posInt[1] > 0:
				if currentRoom.body[posInt[1]-1][posInt[0]+1] != '#' and (charm or (currentRoom.body[posInt[1]-1][posInt[0]] != '#' and currentRoom.body[posInt[1]][posInt[0]+1] != '#')):
					posInt[0] += 1
					posInt[1] -= 1
				elif charm and currentRoom.body[posInt[1]-2][posInt[0]+2] != '#':
					posInt[0] += 2
					posInt[1] -= 2
		elif command == 'b':
			if posInt[0] > 0 and posInt[1] < const.ROOM_HEIGHT - 1:
				if currentRoom.body[posInt[1]+1][posInt[0]-1] != '#' and (charm or (currentRoom.body[posInt[1]+1][posInt[0]] != '#' and currentRoom.body[posInt[1]][posInt[0]-1] != '#')):
					posInt[0] -= 1
					posInt[1] += 1
				elif charm and currentRoom.body[posInt[1]+2][posInt[0]-2] != '#':
					posInt[0] -= 2
					posInt[1] += 2
		elif command == 'n':
			if posInt[0] < const.ROOM_WIDTH - 1 and posInt[1] < const.ROOM_HEIGHT - 1:
				if currentRoom.body[posInt[1]+1][posInt[0]+1] != '#' and (charm or (currentRoom.body[posInt[1]+1][posInt[0]] != '#' and currentRoom.body[posInt[1]][posInt[0]+1] != '#')):
					posInt[0] += 1
					posInt[1] += 1
				elif charm and currentRoom.body[posInt[1]+2][posInt[0]+2] != '#':
					posInt[0] += 2
					posInt[1] += 2

		# Quit and suspend
		elif command == 'q' or command == 'quit':
			if track is not None:
				track.terminate()
			keyListener.stop()
			io.putHighScore('Killed yourself', score)
			rd.highscores(io.getHighScores())
			return
		elif command == 's':
			rd.suspend()

		elif const.DEBUG:
			if command.startswith('d'):
				try:
					depth = int(command[1:])
					currentDepth = gameMap[depth]
					posRooms = list(currentDepth[len(currentDepth) - 1][0])
				except Exception:
					pass

		if didMove:
			explored[depth][posRooms[1]][posRooms[0]] = True # Room is explored
			currentRoom = currentDepth[posRooms[1]][posRooms[0]] # currentRoom is up to date

			if currentDepth[posRooms[1]][posRooms[0]].downstair is not None and posInt[0] == currentDepth[posRooms[1]][posRooms[0]].downstair[0] and posInt[1] == currentDepth[posRooms[1]][posRooms[0]].downstair[1]:
				# Downstairs
				depth += 1
				currentDepth = gameMap[depth]
				posRooms = list(currentDepth[len(currentDepth) - 1][0])
				posInt = list(currentDepth[posRooms[1]][posRooms[0]].entryPoint)
			elif currentDepth[posRooms[1]][posRooms[0]].upstair is not None and posInt[0] == currentDepth[posRooms[1]][posRooms[0]].upstair[0] and posInt[1] == currentDepth[posRooms[1]][posRooms[0]].upstair[1]:
				# Upstairs
				depth -= 1
				currentDepth = gameMap[depth]
				posRooms = list(currentDepth[len(currentDepth) - 1][1])
				posInt = list(currentDepth[posRooms[1]][posRooms[0]].entryPoint)
			elif currentDepth[posRooms[1]][posRooms[0]].exit is not None and posInt[0] == currentDepth[posRooms[1]][posRooms[0]].exit[0] and posInt[1] == currentDepth[posRooms[1]][posRooms[0]].exit[1]:
				io.putHighScore('Left the dungeon', score)
				rd.highscores(io.getHighScores())
				return

		if track is not None:
			if track.poll() is not None:
				track = None
			elif command == 'stop':
				track.terminate()
				track = None
