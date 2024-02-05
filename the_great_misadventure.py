# The idea of this model is to demonstrate world-building capacities beyond text

def initial():
	name = interact.form(['name'])
	return {'name': name}

def step(last_step):
	if not last_step:
		return initial()
	return last_step
