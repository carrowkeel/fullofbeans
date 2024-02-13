import numpy as np

async def run():
	pos = np.array([0.5, 0.5])
	directions = {37: [-1, 0], 38: [0, 1], 39: [1, 0], 40: [0, -1]}
	js.draw('ind', 'scatter_rt', [[[[*pos,1]]]])
	while True:
		arrow = await js.input('keydown', [37, 38, 39, 40])
		direction = np.array(directions[arrow]) * 0.05
		pos = pos + direction
		js.draw('ind', 'scatter_rt', [[[[*pos,1]]]])