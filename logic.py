import os

from room import *
from typing import List, Any
from subprocess import Popen

import random as randLib
import render as rd
import constants as const

def rand(rMin, rMax):
	return randLib.randint(rMin, rMax)

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
		endSide = beginSide + 2 % 4

		if beginSide % 2 is 0:
			beginLoc = (0 if beginSide is 2 else const.MAP_WIDTH - 1, rand(0, const.MAP_HEIGHT - 1))
			endLoc   = (0 if endSide   is 2 else const.MAP_WIDTH - 1, rand(0, const.MAP_HEIGHT - 1))

			currentMap.append([beginLoc, endLoc])

			currentLoc = list(beginLoc if beginLoc is 4 else endLoc)
			finLoc = list(endLoc if endLoc is 2 else beginLoc)

			lastRoom = Room(definitions.PATH)
			lastRoomDir = 4
			while currentLoc != finLoc:
				possibleDirs = None
				if currentLoc[0] is const.MAP_WIDTH - 1: # If on the opposite edge
					possibleDirs = [3 if currentLoc[1] > endLoc[1] else 1] # Move up or down only depending on where we are in relation to the exit
				elif lastRoomDir is 4:
					possibleDirs = [2, 3] if currentLoc[1] is 0 else [1, 2] if currentLoc[1] is const.MAP_HEIGHT else [1, 2, 3] # Move up, down or right randomly
				elif lastRoomDir is 1:
					possibleDirs = [2, 3] if currentLoc[1] is const.MAP_HEIGHT else [1, 2, 3]
				elif lastRoomDir is 3:
					possibleDirs = [1, 2] if currentLoc[1] is 0 else [1, 2, 3]
				else:
					print('An unexpected error occurred while generating the map.')
					exit(1)

				newDir = randLib.choice(possibleDirs)
				if newDir is 1:
					currentLoc[1] -= 1
				elif newDir is 2:
					currentLoc[0] += 1
				elif newDir is 3:
					currentLoc[1] += 1
				else:
					print('An unexpected error occurred while generating the map.')
					exit(1)

				newRoom = Room(definitions.PATH)
				currentMap[currentLoc[1]][currentLoc[0]] = newRoom

				lastRoomDir = newDir + 2 % 4

				lastRoom.neighbours[lastRoomDir] = newRoom
				newRoom.neighbours[newDir] = lastRoom

				lastRoom = newRoom

		else:
			beginLoc = (beginSide, rand(0, const.MAP_WIDTH))
			endLoc = (endSide, rand(0, const.MAP_WIDTH))

			generatedMap.append((beginLoc, endLoc))

			currentLoc = beginLoc
			while currentLoc != endLoc:
				break

		generatedMap.append(currentMap)

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
