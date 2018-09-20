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

###

def get_final_path(ending_node):

	current = ending_node
	nodes = []

	while(current != None):
		nodes.append(current)
		current = current.from_node

	nodes = nodes[::-1]
	print('\nSTART')
	print(nodes[0].state.reshape(3, 4))
	for node in nodes[1:]:
		print(node.from_move)
		print(node.state.reshape(3, 4))
	print('\nGOAL STATE FOUND! CONGRATULATIONS\n')

def build_children(node, closed_list):
		
	moves = get_legal_moves(node.state, closed_list)
	children = []

	for move in moves:
		children.append(Node(move[0], h2(move[0]), node.depth + 1, node, move[1]))
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

class AStar():

	def __init__(self, initial_state):
		self.open_list = []
		self.closed_list = pd.DataFrame({'State' : [str([0]*12)]})
		self.head_node = Node(initial_state, h2(initial_state), 0, None)
		self.num_searches = 0

	def build_children(node, closed_list):
		
		moves = get_legal_moves(node.board, closed_list)
		children = []

		for move in moves:
			children.append(Node(move, h2(move)+node.cost, node.depth + 1, node))
		return children

	def traversal(self):

		current_position = self.head_node

		while(True):

			if(current_position.is_goal_state()):
				print(self.num_searches)
				print('STATE FINISHED')
				break

			children = build_children(current_position, self_closed_list)
			children = [child for child in children if child.cost < current_position]
			if(len(children) != 0):
				self.open_list = children + self.open_list

class BestFirst():

	def __init__(self, initial_state):
		self.open_list = []
		self.closed_list = pd.DataFrame({'State' : [str([0]*12)]})
		self.head_node = Node(initial_state, h2(initial_state), 0)
		self.num_searches = 0

	def traversal(self):

		current_position = self.head_node
		counter = 0

		while(True):

			if(current_position.is_goal_state()):
				print(counter)
				print('STATE FINISHED')
				break

			children = build_children(current_position, self.closed_list)
			children = []
			if(current_position.cost > min([child.cost for child in children] + [current_position.cost])):
				self.open_list = children + self.open_list

			self.closed_list = self.closed_list.append({'State' : str(list(current_position.board))}, 
													   ignore_index=True)
			costs = [node.cost for node in self.open_list]
			idc = np.argsort(costs)
			self.open_list = np.array(self.open_list)[idc].tolist()
			current_position = self.open_list[0]
			del self.open_list[0]

class Node():

	def __init__(self, state, cost, depth, from_node, from_move):

		self.state = state
		self.cost = cost
		self.depth = depth
		self.from_node = from_node
		self.from_move = move_dict[str(from_move)]

	def is_goal_state(self):
		return np.array_equal(self.state, np.append(np.arange(1, 12), 0))

class BFS():

	def __init__(self, initial_state, max_depth):
		self.open_list = []
		self.closed_list = pd.DataFrame({'State' : [str([0]*12)]})
		self.head_node = Node(initial_state, 0, 0, None, 'START')
		self.max_depth = max_depth
		self.search_moves = 0

	def traversal(self):

		current_position = self.head_node

		while(True):

			if(current_position.is_goal_state()):
				print('Number of Searches:',self.search_moves)
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
			print('Search Moves', self.search_moves)
			print('Depth', current_position.depth)
			self.search_moves += 1

if __name__ == '__main__':

	states = np.load('Data/states.npy')
	bfs = BFS(np.array([1, 6, 4, 0, 5, 3, 2, 8, 9, 10, 11, 7]), 3)
	bfs.traversal()





