import os

from room import *
from typing import List, Any
from subprocess import Popen

import random as randLib
import render as rd
import constants as const

def rand(rMin, rMax):
	return randLib.randint(rMin, rMax)

def log(*values):
	if const.DEBUG:
		print(*values)

def generateMap(difficulty, seed = randLib.seed):
	randLib.seed(seed)

	generatedMap: List[List[Any]] = []

	for depth in range(const.MAX_DEPTH):
		currentMap: List[List[Any]] = []

		# Generate the indices for this depth
		for y in range(const.MAP_HEIGHT):
			currentMap.append([])
			for x in range(const.MAP_WIDTH):
				currentMap[y].append(None)

		# 1 = N, 2 = E, 3 = S, 4 = W
		beginSide = rand(1, 4) if depth is not 0 else 3
		endSide = (beginSide + 2) % 4

		if beginSide % 2 is 0:
			beginLoc = (0 if beginSide is 2 else const.MAP_WIDTH - 1, rand(0, const.MAP_HEIGHT - 1))
			endLoc   = (0 if endSide   is 2 else const.MAP_WIDTH - 1, rand(0, const.MAP_HEIGHT - 1))

			currentMap.append([beginLoc, endLoc])

			currentLoc = list(beginLoc if beginSide is 4 else endLoc)
			finLoc = list(endLoc if endSide is 2 else beginLoc)

			log(currentLoc)
			log(finLoc)

			lastRoom = None
			lastRoomDir = 4
			while not (currentLoc.x == finLoc.x and currentLoc.y == finLoc.y):
				possibleDirs = None
				if currentLoc[0] is const.MAP_WIDTH - 1: # If on the opposite edge
					possibleDirs = [3 if currentLoc[0] > finLoc[0] else 1] # Move up or down only depending on where we are in relation to the exit
				elif lastRoomDir is 2:
					possibleDirs = [2, 3] if currentLoc[1] is 0 else ([1, 2] if currentLoc[1] is const.MAP_HEIGHT - 1 else [1, 2, 3]) # Move up, down or right randomly according to the bounds of the map
				elif lastRoomDir is 3:
					possibleDirs = [2] if currentLoc[1] is const.MAP_HEIGHT - 1 else [1, 2]
				elif lastRoomDir is 1:
					possibleDirs = [2] if currentLoc[1] is 0 else [2, 3]
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

				log(currentLoc, newDir)

				newRoom = Room(currentLoc[0], currentLoc[1], definitions.PATH)
				currentMap[currentLoc[1]][currentLoc[0]] = newRoom

				if lastRoom is not None:
					lastRoom.neighbours[newDir - 1] = newRoom
					newRoom.neighbours[(newDir + 2) % 4 - 1] = lastRoom

				lastRoom = newRoom
				lastRoomDir = newDir

		else:
			beginLoc = (rand(0, const.MAP_WIDTH - 1), 0 if beginSide is 1 else const.MAP_HEIGHT - 1)
			endLoc   = (rand(0, const.MAP_WIDTH - 1), 0 if endSide   is 1 else const.MAP_HEIGHT - 1)

			currentMap.append([beginLoc, endLoc])

			currentLoc = list(beginLoc if beginSide is 1 else endLoc)
			finLoc = list(endLoc if endSide is 3 else beginLoc)

			log(currentLoc)
			log(finLoc)

			lastRoom = None
			lastRoomDir = 4
			while not (currentLoc.x == finLoc.x and currentLoc.y == finLoc.y):
				possibleDirs = None
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

				log(currentLoc, newDir)

				newRoom = Room(currentLoc[0], currentLoc[1], definitions.PATH)
				currentMap[currentLoc[1]][currentLoc[0]] = newRoom

				if lastRoom is not None:
					lastRoom.neighbours[newDir - 1] = newRoom
					newRoom.neighbours[(newDir + 2) % 4 - 1] = lastRoom

				lastRoom = newRoom
				lastRoomDir = newDir

		generatedMap.append(currentMap)

def roomToInt(room: Room, pos: List[int]) -> int:
	i = 0
	if room.x is pos[0] and room.y is pos[1]:
		i = 0b10000000

	return i

def playGame(gameMap):
	health = const.START_HEALTH
	armour = const.START_ARMOUR
	attack = const.START_ATTACK
	explored = []

	# Generate explored map
	for y in range(len(gameMap)):
		explored.append([])
		for x in range(len(gameMap[y])):
			explored[y].append(False)

	track: Popen = None
	filePath = os.path.dirname(os.path.realpath(__file__))

	# Main loop
	while True:
		rd.header()
		rd.stats(health, armour, attack)

		rd.rooms

		command = input("> ")

		# Music commands
		if command == 'mglvna':
			if track is not None:
				track.terminate()

			# Megalovania but every other beat was removed
			track = Popen(['/usr/bin/afplay', filePath + '/data/msc(idn.mp3'])
		elif command == 'megalovania':
			if track is not None:
				track.terminate()

			# Megalovania
			track = Popen(['/usr/bin/afplay', filePath + '/data/music (hidden).mp3'])

		# Cheat codes
		elif command == 'winxp':
			for y in range(len(explored)):
				for x in range(len(explored[y])):
					explored[y][x] = True
		elif command == 'kkjjhlhlba':
			pass

		elif command == 'quit':
			if track is not None:
				track.terminate()
			return # Make this more than just a quit

		if track is not None:
			if track.poll() is not None:
				track = None
			elif command == 'stop':
				track.terminate()
				track = None
