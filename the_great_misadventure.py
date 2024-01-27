# Der Spiegel im Spiegel

def initial():
	name = interact.form(['name'])
	return {'name': name}

def step(last_step):
	if not last_step:
		return initial()
	return last_step
