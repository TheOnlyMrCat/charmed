from typing import List, Tuple

import csv
import os


def getHighScores() -> List[Tuple[str, int]]:
	if not os.path.isfile('data/highscores.csv'):
		open('data/highscores.csv', 'x').close()

	table = []
	with open('data/highscores.csv', newline='') as highscores:
		reader = csv.reader(highscores)
		for row in reader:
			table.append((row[0], row[1]))
	return sorted(table, key=lambda x: int(x[1]), reverse=True)


def putHighScore(lastAct: str, score: int):
	if not os.path.isfile('data/highscores.csv'):
		open('data/highscores.csv', 'x').close()
	with open('data/highscores.csv', 'a') as highscores:
		highscores.write(lastAct + ',' + str(score) + '\n')


def clearHighScores():
	open('data/highscores.csv', 'w').close()
