import numpy as np
import pandas as pd
import time

### MOVES ###

move_dict = {'[-1, -1]' : 'UP-LEFT', 
			 '[-1, 0]' : 'UP', 
			 '[-1, 1]' : 'UP-RIGHT', 
			 '[0, 1]' : 'RIGHT', 
			 '[1, 1]' : 'DOWN-RIGHT', 
			 '[1, 0]' : 'DOWN', 
			 '[1, -1]' : 'DOWN-LEFT', 
			 '[0, -1]' : 'LEFT', 
			 'START' : 'START'}

###

### HEURISTICS ### 

def h1(board_state):
	goal_state = np.append(np.arange(1, 12), 0)
	return 12 - np.where(goal_state == board_state)[0].shape[0]

def h1_mod(board_state):
    board_state = board_state.tolist()
    cost = [abs(board_state.index(i) - i + 1) for i in range(1, 12)]
    cost = cost + [abs(11 - board_state.index(0))]
    return sum(cost)

def h2(board_state):
    board_state = board_state.reshape(3, 4)
    goal_state = np.append(np.arange(1, 12), 0).reshape(3, 4)
    cost = 0
    for i in goal_state.ravel():
        idx_board = np.argwhere(board_state==i)[0]
        idx_goal = np.argwhere(goal_state==i)[0]
        cost += sum(abs(idx_board - idx_goal))
    return cost

def h2_mod(board_state):
    board_state = board_state.reshape(3, 4)
    goal_state = np.append(np.arange(1, 12), 0).reshape(3, 4)
    cost = 0
    for i in goal_state.ravel():
        idx_board = np.argwhere(board_state==i)[0]
        idx_goal = np.argwhere(goal_state==i)[0]
        cost += max(abs(idx_board - idx_goal))
    return cost

def h3(board_state):
    goal_state = np.append(np.arange(1, 12), 0).reshape(3, 4)
    board_state = board_state.reshape(3, 4)
    goal_sum = np.append(goal_state.sum(axis=0)/3, goal_state.sum(axis=1)/4)
    board_sum = np.append(board_state.sum(axis=0)/3, board_state.sum(axis=1)/4)
    return np.sqrt(np.sum(np.power(board_sum - goal_sum, 2)))

def O2(board_state):
    l1_cost = h2(board_state)
    moves = get_legal_moves(board_state)
    l2_cost = min([h2(move[0]) for move in moves])
    return l1_cost+l2_cost

###

func = h2

def get_final_path(ending_node):

	current = ending_node
	nodes = []

	while(current != None):
		nodes.append(current)
		current = current.from_node

	nodes = nodes[::-1]
	print()
	for node in nodes:
		print(node.from_move)
		print(node.state.reshape(3, 4))
	print('\nGOAL STATE FOUND! CONGRATULATIONS\n')

def build_children(node, closed_list):
		
	moves = get_legal_moves(node.state, closed_list)
	children = []

	for move in moves:
		children.append(Node(move[0], func(move[0]), node.depth + 1, node, move[1]))
	return children

def get_legal_moves(board_state, closed_list):

	idc = [[1, -1], [1, 0], [1, 1], 
	       [-1, 1], [-1, 0], [-1, -1], 
	       [0, 1], [0, -1]]

	board_state = board_state.reshape(3, 4)
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
					legal_moves.append([new_state.ravel(), idx])

		except Exception as e:
			pass
		
	return legal_moves

class BFS():

	def __init__(self, initial_state, max_depth):
		self.open_list = []
		self.closed_list = pd.DataFrame({'State' : [str([0]*12)]})
		self.head_node = Node(initial_state, 0, 0, None, 'START')
		self.max_depth = max_depth
		self.searches = 0

	def traversal(self):

		current_position = self.head_node

		while(True):

			if(current_position.is_goal_state()):
				print('Number of Searches:',self.searches)
				get_final_path(current_position)
				break

			if(current_position.depth < self.max_depth):
				children = build_children(current_position, self.closed_list)
				self.open_list = children + self.open_list

			self.closed_list = self.closed_list.append({'State' : str(list(current_position.state))}, 
													   ignore_index=True)
			try:
				current_position = self.open_list[0]
				del self.open_list[0]
			except:
				print('\nNO SOLUTIONS FOUND - OPEN LIST EMPTY\n')
				break

			print(' - - - - - -  - - ')
			print('Search Moves', self.searches)
			print('Depth', current_position.depth)
			self.searches += 1

class BestFirst():

	def __init__(self, initial_state):
		self.open_list = []
		self.closed_list = pd.DataFrame({'State' : [str([0]*12)]})
		self.head_node = Node(initial_state, func(initial_state), 0, None, 'START')
		self.searches = 0

	def traversal(self):

		current_position = self.head_node

		while(True):

			if(current_position.is_goal_state()):
				print('Number of Searches:', self.searches)
				get_final_path(current_position)
				break

			print(' - - - - - -  - - ')
			print('Searches:', self.searches)
			print('Depth:', current_position.depth)
			print('Cost:', current_position.cost)

			children = build_children(current_position, self.closed_list)
			self.open_list = children + self.open_list
			self.closed_list = self.closed_list.append({'State' : str(list(current_position.state))}, 
													   ignore_index=True)
			costs = [node.cost for node in self.open_list]
			idc = np.argsort(costs)
			self.open_list = np.array(self.open_list)[idc].tolist()

			try:
				current_position = self.open_list[0]
				del self.open_list[0]
			except:
				print('\nNO SOLUTIONS FOUND - OPEN LIST EMPTY\n')
				break

			self.searches += 1

class Node():

	def __init__(self, state, cost, depth, from_node, from_move):

		self.state = state
		self.cost = cost
		self.depth = depth
		self.from_node = from_node
		self.from_move = move_dict[str(from_move)]

	def is_goal_state(self):
		return np.array_equal(self.state, np.append(np.arange(1, 12), 0))

class AStar():

	def __init__(self, initial_state):
		self.open_list = []
		self.head_node = Node(initial_state, func(initial_state), 0, None, 'START')
		self.searches = 0

	def build_children(self, node):
		
		moves = self.get_legal_moves(node.state)
		children = []

		for move in moves:
			children.append(Node(move[0], func(move[0])+node.depth, node.depth + 1, node, 
								 move[1]))
		return children

	def get_legal_moves(self, board_state):

		idc = [[1, -1], [1, 0], [1, 1], 
		       [-1, 1], [-1, 0], [-1, -1], 
		       [0, 1], [0, -1]]

		board_state = board_state.reshape(3, 4)
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
					legal_moves.append([new_state.ravel(), idx])
			except Exception as e:
				pass
			
		return legal_moves

	def traversal(self):

		current_position = self.head_node

		while(True):

			if(current_position.is_goal_state()):
				print('Number of Searches:', self.searches)
				get_final_path(current_position)
				break

			print(' - - - - - -  - - ')
			print('Searches:', self.searches)
			print('Depth:', current_position.depth)
			print('Cost:', current_position.cost)

			children = self.build_children(current_position)
			self.open_list = children + self.open_list
			costs = [node.cost for node in self.open_list]
			idc = np.argsort(costs)
			self.open_list = np.array(self.open_list)[idc].tolist()

			try:
				current_position = self.open_list[0]
				del self.open_list[0]
			except:
				print('\nNO SOLUTIONS FOUND - OPEN LIST EMPTY\n')
				break

			self.searches += 1

if __name__ == '__main__':

	states = np.load('Data/states.npy')
	#bfs = BestFirst(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 11]))
	bfs = BestFirst(states[1])
	#bfs = BestFirst(states[1])
	bfs.traversal()





