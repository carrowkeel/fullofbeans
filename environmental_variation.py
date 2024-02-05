# This test model was designed to test your patience
# I am here to reassure you that this is real

import numpy as np
from time import sleep

def defaults():
	return {
		's': 0.5,
		'c': 1,
		'h': 0.5,
		'q0': 0.8,
		'm': 0.01,
		'm_inf': 0,
		's_var': 0.4,
		'grid_size': 21,
		'repeats': 1,
		'target': 221,
		'target_steps': 200
	}

def generate_graph_from_grid(n):
	mat_n = n**2
	M = np.zeros([mat_n, mat_n])
	main_diag = np.diag_indices(mat_n, 2)
	d1 = np.array([main_diag[0][:-1], main_diag[1][1:]]).T
	d2 = np.array([main_diag[0][:-n], main_diag[1][n:]]).T
	M[d1[:,0], d1[:,1]] = 1
	M[d2[:,0], d2[:,1]] = 1
	M[d1[:,0][n-1::n], d1[:,1][n-1::n]] = 0
	nodes = np.indices((n, n)).T.reshape(n * n, 2) / n
	return M + M.T, nodes

def generate_graph(params):
	return generate_graph_from_grid(params['grid_size'])

def migration_network(params, graph):
	n = graph.shape[0]
	M = graph * params['m'] + params['m_inf'] / n
	M[range(n), range(n)] = 0
	M[range(n), range(n)] = 1 - np.sum(M, axis=1)
	return M

def initial():
	params = defaults() ## Here could try to get params from user
	edges, nodes = generate_graph(params)
	M = migration_network(params, edges)
	q = np.zeros(M.shape[0])
	s = np.full(M.shape[0], params['s']) if params['s_var'] == 0 else np.clip(np.random.normal(loc=params['s'], scale=params['s_var'], size=M.shape[0]), 0, 1)
	q[params['target']] = params['q0']
	##nodes_q = np.insert(nodes, 2, np.maximum(q, 0.1), axis=1) if len(nodes) > 0 else np.ndarray([0,3])
	return {'params': params, 'q': q, 'M': M, 's_nodes': s, 'topology': nodes}

def step(last_step, t):
	if not last_step:
		return initial()
	params = last_step['params']
	if params['target_steps'] == t:
		return False
	q = np.array(last_step['q'])
	M = np.array(last_step['M']) ## Migration network, generated in first step by "initial"
	s = np.array(last_step['s_nodes'])
	c = params['c']
	h = params['h']
	s_c = (1 - s) * c
	s_n = 0.5 * (1 - h * s) * (1 - c)
	q_tilde = np.dot(q, M)
	w_bar = q_tilde**2 * (1 - s) + 2 * q_tilde * (1 - q_tilde) * (s_c + 2 * s_n) + (1 - q_tilde)**2
	q_tag = (q_tilde**2 * (1 - s) + 2 * q_tilde * (1 - q_tilde) * (s_c + s_n)) / w_bar
	nodes_q = np.insert(last_step['topology'], 2, np.maximum(q_tag, 0.1), axis=1) if len(last_step['topology']) > 0 else np.ndarray([0,3])
	spillover_prev = len(q[q >= 0.5]) / M.shape[0]
	spillover = len(q_tag[q_tag >= 0.5]) / M.shape[0]
	js.draw('q_spatial', 'scatter_rt', [[nodes_q]])
	js.draw('spillover', 'line_plot_x', [[[t / params['target_steps'], spillover_prev]],[[(t + 1) / params['target_steps'], spillover]]])
	sleep(0.01)
	return {'params': params, 'q': q_tag, 'M': M, 's_nodes': s, 'topology': last_step['topology']}

async def run():
	last_step = None
	t = 0
	while last_step != False:
		last_step = step(last_step, t)
		t += 1
	return True
