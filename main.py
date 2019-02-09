import render
import constants as const
import logic

def main():
	print('\x1b[0;97;40', end='')
	const.DEBUG = render.welcome()
	difficulty = int(render.difficulty())
	seed = render.seed()

	if seed != '':
		render.generating(seed)
		gameMap = logic.generateMap(difficulty, seed)
	else:
		render.generating()
		gameMap = logic.generateMap(difficulty)

	logic.playGame(gameMap)

if __name__ == "__main__":
	main()
