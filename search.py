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
	return len(nodes)

def build_children(node, closed_list, func, heuristic_time):
		
	moves = get_legal_moves(node.state, closed_list)
	children = []

	for move in moves:
		start = time.time()
		cost = func(move[0])
		heuristic_time.append(time.time() - start)
		children.append(Node(move[0], cost, node.depth + 1, node, move[1]))
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

	def __init__(self, initial_state, max_depth, func):
		self.open_list = []
		self.func = func
		self.closed_list = pd.DataFrame({'State' : [str([0]*12)]})
		self.head_node = Node(initial_state, 0, 0, None, 'START')
		self.max_depth = max_depth
		#Stats
		self.searches = 0
		self.overall_time = 0
		self.solution_path_length = 0
		self.costs = []
		self.depths = []
		self.heuristic_time = []

	def traversal(self):

		current_position = self.head_node
		self.overall_time = time.time()

		while(True):

			if(current_position.is_goal_state()):
				print('Number of Searches:',self.searches)
				self.solution_path_length = get_final_path(current_position)
				self.overall_time -= (self.overall_time-time.time())
				break

			print(' - - - - - -  - - ')
			print('Searches:', self.searches)
			print('Depth:', current_position.depth)
			print('Cost:', current_position.cost)
			print('HTime:', len(self.heuristic_time))
			self.costs.append(current_position.cost)
			self.depths.append(current_position.depth)	

			if(current_position.depth < self.max_depth):
				children = build_children(current_position, self.closed_list, 
										  self.func, self.heuristic_time)
				self.open_list = children + self.open_list

			self.closed_list = self.closed_list.append({'State' : str(list(current_position.state))}, 
													   ignore_index=True)
			try:
				current_position = self.open_list[0]
				del self.open_list[0]
			except:
				print('\nNO SOLUTIONS FOUND - OPEN LIST EMPTY\n')
				self.overall_time = -1
				break

			self.searches += 1

class BestFirst():

	def __init__(self, initial_state, func):
		self.open_list = []
		self.func = func
		self.closed_list = pd.DataFrame({'State' : [str([0]*12)]})
		self.head_node = Node(initial_state, func(initial_state), 0, None, 'START')
		#Stats
		self.searches = 0
		self.overall_time = 0
		self.solution_path_length = 0
		self.costs = []
		self.depths = []
		self.heuristic_time = []

	def traversal(self):

		current_position = self.head_node
		self.overall_time = time.time()

		while(True):

			if(current_position.is_goal_state()):
				print(' - - - - - -  - - ')
				print('\nNumber of Searches:', self.searches)
				self.solution_path_length = get_final_path(current_position)
				self.overall_time -= (self.overall_time-time.time())
				break

			###
			print(' - - - - - -  - - ')
			print('Searches:', self.searches)
			print('Depth:', current_position.depth)
			print('Cost:', current_position.cost)
			print('HTime:', len(self.heuristic_time))
			self.costs.append(current_position.cost)
			self.depths.append(current_position.depth)
			###

			self.closed_list = self.closed_list.append({'State' : str(list(current_position.state))}, 
													   ignore_index=True)

			children = build_children(current_position, self.closed_list, 
									  self.func, self.heuristic_time)
			self.open_list = children + self.open_list
			costs = [node.cost for node in self.open_list]
			idc = np.argsort(costs)
			self.open_list = np.array(self.open_list)[idc].tolist()

			try:
				current_position = self.open_list[0]
				del self.open_list[0]
			except:
				print('\nNO SOLUTIONS FOUND - OPEN LIST EMPTY\n')
				self.overall_time = -1
				break

			self.searches += 1

class AStar():

	def __init__(self, initial_state, func):
		self.open_list = []
		self.func = func
		self.head_node = Node(initial_state, func(initial_state), 0, None, 'START')
		#Stats
		self.searches = 0
		self.solution_path_length = 0
		self.overall_time = 0
		self.costs = []
		self.depths = []
		self.heuristic_time = []

	def build_children(self, node):
		
		moves = self.get_legal_moves(node.state)
		children = []

		for move in moves:
			start = time.time()
			cost = self.func(move[0])+node.depth
			self.heuristic_time.append(time.time() - start)
			children.append(Node(move[0], cost, node.depth + 1, node, 
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
		self.overall_time = time.time()

		while(True):

			if(current_position.is_goal_state()):
				print(' - - - - - -  - - ')
				print('\nNumber of Searches:', self.searches)
				self.solution_path_length = get_final_path(current_position)
				self.overall_time -= (self.overall_time-time.time())
				break

			print(' - - - - - -  - - ')
			print('Searches:', self.searches)
			print('Depth:', current_position.depth)
			print('Cost:', current_position.cost)
			print('HTime:', len(self.heuristic_time))
			self.costs.append(current_position.cost)
			self.depths.append(current_position.depth)

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
				self.overall_time = -1
				break

			self.searches += 1





