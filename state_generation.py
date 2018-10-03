import numpy as np
import pandas as pd
from argparse import ArgumentParser
import time

size_one = 3
size_two = 4

def get_legal_moves(board_state, closed_list):

	idc = [[1, -1], [1, 0], [1, 1], 
	       [-1, 1], [-1, 0], [-1, -1], 
	       [0, 1], [0, -1]]

	board_state = board_state.reshape(size_one, size_two)
	empty_index = np.argwhere(board_state == 0)[0]
	legal_moves = []

	for idx in idc:
		try:
			pos = empty_index + idx
			if(len([i for i in pos if i >= 0])==2):
				new_state = board_state.copy()
				new_state[empty_index[0],
						  empty_index[1]] = new_state[pos[0], pos[1]]
				new_state[pos[0], pos[1]] = 0
				
				if(closed_list[closed_list.State 
									== str(new_state.ravel().tolist())].shape[0] == 0):
					legal_moves.append(new_state.ravel())

		except Exception as e:
			pass
		
	return legal_moves

def generate_board_state(difficulty):

	current_state = np.append(np.arange(1, size_one*size_two), 0)
	closed_list = pd.DataFrame({'State' : [str([0]*(size_one*size_two))]})

	for i in range(difficulty):

		moves = get_legal_moves(current_state, closed_list)
		idx = np.random.permutation(len(moves))[0]
		current_state = moves[idx]
		closed_list = closed_list.append({'State' : str(list(current_state))}, 
										 ignore_index=True)

	return current_state

if __name__ == '__main__':

	parser = ArgumentParser(description='Script to generate solvable board states. The difficulties are 5, 10, 15, 20, 25, 30')
	parser.add_argument('N', help='Number of states to generate.', type=int, default=20)

	args = parser.parse_args()
	#diffs = [5, 10, 15, 20, 25, 30]
	diffs = [2, 3, 4, 5, 6, 8, 10, 12]
	difficulties, states = [], []
	start = time.time()

	for i in range(args.N):
		try:
			print('Progress %.3f' % (i / args.N))
			states.append(generate_board_state(diffs[i % len(diffs)]))
			difficulties.append(diffs[i % len(diffs)])
		except Exception as e:
			print(e)

	np.save('Data/states_bfs.npy', states)
	np.save('Data/diffs_bfs.npy', diffs)
	print(time.time() - start)

