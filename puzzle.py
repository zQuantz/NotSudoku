import numpy as np

class Puzzle():

	def __init__(self):

		self.board = self.random_state
		self.initial_state = self.board
		self.num_moves = 0
		self.goal_state = np.arange(1, 12).tolist() + [0]

	def random_state():

		return np.random.permutation(size=12).reshape(3, 4)

	def get_possible_moves(self, empty_index):

		idc = [[1, -1], [1, 0], [1, 1], 
		       [-1, 1], [-1, 0], [-1, -1], 
		       [0, 1], [0, -1]]

		legal_moves = []

		for idx in idc:

			try:
				self.board[empty_index+idx]
				legal_moves.append(empty_index+idx)
			except:
				pass

		return legal_moves

