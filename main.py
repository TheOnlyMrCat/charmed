import render
import constants as const
import logic
import subprocess

def main():
	opts = render.welcome()
	const.DEBUG = 'k' in opts
	difficulty = int(render.difficulty()) if 'd' in opts else 2
	seed = render.seed() if 's' in opts else ''

	if "'" not in opts: render.tutorial()

	if seed != '':
		render.generating(seed)
		gameMap = logic.generateMap(difficulty, seed)
	else:
		render.generating()
		gameMap = logic.generateMap(difficulty)

	logic.playGame(gameMap)
	render.thankyou()

if __name__ == "__main__":
	main()
