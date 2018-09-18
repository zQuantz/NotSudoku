import numpy as np
import pandas as pd
import time

class Node():

	def __init__(self, board, cost, depth):

		self.board = board
		self.cost = cost
		self.depth = depth
		self.children = []

	def is_goal_state(self):

		return np.array_equal(self.board, np.arange(1, 12).tolist() + [0])

def h1():
	pass

def h2():
	pass

class BFS():

	def __init__(self, initial_state, max_depth):
		self.open_list = []
		self.closed_list = pd.DataFrame({'State' : [str([0]*12)]})
		## APPLY COST
		self.head_node = Node(initial_state, 0, 0)
		self.moves = 0
		self.max_depth = max_depth

	def traversal(self):

		current_position = self.head_node
		counter = 0

		while(True):

			print('11-D Puzzle - Uninformed Search')
			print(current_position.board.reshape(3, 4))
			print()

			if(current_position.is_goal_state()):
				print(counter)
				print('STATE FINISHED')
				break

			if(current_position.depth < self.max_depth):
				children = self.build_children(current_position)
				self.open_list = children + self.open_list

			self.closed_list = self.closed_list.append({'State' : str(list(current_position.board))}, 
													   ignore_index=True)
			print('Depth', current_position.depth)
			print('Nodes', len(self.open_list))
			current_position = self.open_list[0]
			del self.open_list[0]
			counter += 1


	def build_children(self, node):
		
		moves = self.get_legal_moves(node.board)
		children = []

		for move in moves:
			children.append(Node(move, 0, node.depth + 1))

		return children

	def get_legal_moves(self, board_state):

		idc = np.array([[1, -1], [1, 0], [1, 1], 
		       [-1, 1], [-1, 0], [-1, -1], 
		       [0, 1], [0, -1]])

		board_state = board_state.reshape(3, 4)
		empty_index = np.argwhere(board_state == 0)[0]
		legal_moves = []

		for idx in idc[np.random.permutation(len(idc))]:
			try:
				pos = empty_index + idx
				if(len([i for i in pos if i >= 0])==2):
					new_state = board_state.copy()
					new_state[empty_index[0],
							  empty_index[1]] = new_state[pos[0], pos[1]]
					new_state[pos[0], pos[1]] = 0

					if(self.closed_list[self.closed_list.State 
										== str(new_state.ravel().tolist())].shape[0] == 0):
						legal_moves.append(new_state.ravel())
			except:
				pass

		return legal_moves

if __name__ == '__main__':

	bfs = BFS(np.random.permutation(12), 75)
	bfs.traversal()





