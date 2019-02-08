import render
import constants as const
import logic

def main():
	print('\x1b[0;97;40', end='')
	const.DEBUG = render.welcome()
	difficulty = int(render.difficulty())
	seed = render.seed()

	if seed != '':
		logic.playGame(logic.generateMap(difficulty, seed))
	else:
		logic.playGame(logic.generateMap(difficulty))

if __name__ == "__main__":
	main()
