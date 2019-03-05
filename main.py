import render
import os
import constants as const
import logic
import fileio


def main():
	try:
		cont = True
		while cont:
			cont = False
			opts = render.welcome()
			const.DEBUG = 'k' in opts
			if 'h' in opts:
				render.highscores(fileio.getHighScores())
			else:
				difficulty = int(render.difficulty()) if 'd' in opts else 2
				seed = render.seed() if 's' in opts else ''

				if "'" not in opts:
					render.tutorial()
					render.commands()

				if seed != '':
					render.generating(seed)
					gameMap = logic.generateMap(difficulty, seed)
				else:
					seed = str(int.from_bytes(os.urandom(4), 'big'))

					render.generating()
					gameMap = logic.generateMap(difficulty, seed)

				logic.playGame(gameMap, difficulty, seed)

			cont = render.cont()
			render.thankyou()
	except Exception:
		print('An error occurred. Send the seed and the following error message to the developer for his unforgivable mistake.')
		print('Seed: ' + str(seed))
		raise
	finally:
		input('Press enter to exit.')
		print('\x1b[0m')  # Reset terminal colours


if __name__ == "__main__":
	main()
