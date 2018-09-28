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

tile_dict = {0 : 'a', 1 : 'b', 
			 2 : 'c', 3 : 'd', 
			 4 : 'e', 5 : 'f', 
			 6 : 'g', 7 : 'h', 
			 8 : 'i', 9 : 'j', 
			 10 : 'k', 11 : 'l'}
###

class Node():

	def __init__(self, state, cost, depth, from_node, from_move):

		self.state = state
		self.cost = cost
		self.depth = depth
		self.from_node = from_node
		self.from_move = move_dict[str(from_move)]

	def is_goal_state(self):
		return np.array_equal(self.state, np.append(np.arange(1, 12), 0))

class Search():

	def __init__(self, max_searches=15000, outfile=None):
		self.open_list = []
		self.closed_list = pd.DataFrame({'State' : [str([0]*12)]})
		self.outfile = outfile
		self.max_searches = max_searches
		#Stats
		self.reset_statistics()

	def reset_statistics(self):
		self.searches = 0
		self.overall_time = 0
		self.solution_path_length = 0
		self.costs = []
		self.depths = []
		self.heuristic_time = []

	def get_final_path(self, ending_node):

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
		return len(nodes), nodes

	def build_children(self, node, func=None):
			
		moves = self.get_legal_moves(node.state)
		children = []

		for move in moves:
			start = time.time()
			cost = func(move[0]) if func != None else 0
			cost += node.depth if self.closed_list.shape[0] == 0 else 0
			self.heuristic_time.append(time.time() - start)
			children.append(Node(move[0], cost, node.depth + 1, node, move[1]))
		return children

	def get_legal_moves(self, board_state):

		idc = [[-1, 0], [-1, 1], [0, 1], 
			   [1, 1], [1, 0], [1, -1], 
			   [0, -1], [-1, -1]]

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

					if(1 if self.closed_list.shape[0] == 0 else self.closed_list[self.closed_list.State 
														  == str(new_state.ravel().tolist())].shape[0] == 0):
						legal_moves.append([new_state.ravel(), idx])
			except Exception as e:
				pass
			
		return legal_moves

	def save_solution(self, nodes):

		with open(self.outfile, 'w') as file:

			file.write('%d %s\n' % (0, nodes[0].state))

			for node in nodes[1:]:

				idx = np.argwhere(node.state == 0)[0][0]

				file.write('%s %s\n' % (tile_dict[idx], node.state))

	def evaluate(self, current_position, func=None):

		pass

	def traversal(self, initial_state, func=None):

		self.reset_statistics()
		current_position = Node(initial_state, 0 if func == None else func(initial_state), 
								0, None, 'START')  
		self.overall_time = time.time()

		while(True):

			if(current_position.is_goal_state()):
				print('Number of Searches:', self.searches)
				self.solution_path_length, nodes = self.get_final_path(current_position)
				self.overall_time -= (self.overall_time-time.time())
				if(self.outfile != None):
					self.save_solution(nodes)
				break
			
			print(' - - - - - -  - - ')
			print('Searches:', self.searches)
			print('Depth:', current_position.depth)
			print('Cost:', current_position.cost)
			print('HTime:', len(self.heuristic_time))
			
			self.costs.append(current_position.cost)
			self.depths.append(current_position.depth)

			self.evaluate(current_position, func=func)

			try:
				current_position = self.open_list[0]
				del self.open_list[0]
			except:
				print('\nNO SOLUTIONS FOUND - OPEN LIST EMPTY\n')
				self.overall_time = -1
				break

			self.searches += 1

			if(self.searches == self.max_searches):
				print('NO SOLUTIONS FOUND - MAX SEARCHES REACHED')
				self.overall_time = -2
				break

class BFS(Search):

	def __init__(self, max_searches=15000, max_depth=None, outfile=None):
		Search.__init__(self, max_searches=max_searches, outfile=outfile)
		self.max_depth = max_depth
		self.max_depth_list = []

	def evaluate(self, current_position, func):
		if(True if self.max_depth == None else current_position.depth <= self.max_depth):
			children = self.build_children(current_position, func=None)
			self.open_list = children + self.open_list
			if(self.max_depth != None) & (current_position.depth == self.max_depth):
				self.max_depth_list.append(current_position)

	def traversal(self, initial_state, func=None):

		self.reset_statistics()
		current_position = Node(initial_state, 0 if func == None else func(initial_state), 
								0, None, 'START')  
		self.overall_time = time.time()

		while(True):

			if(current_position.is_goal_state()):
				print('Number of Searches:', self.searches)
				self.solution_path_length, nodes = self.get_final_path(current_position)
				self.overall_time -= (self.overall_time-time.time())
				if(self.outfile != None):
					self.save_solution(nodes)
				break
			'''
			print(' - - - - - -  - - ')
			print('Searches:', self.searches)
			print('Depth:', current_position.depth)
			print('Cost:', current_position.cost)
			print('HTime:', len(self.heuristic_time))
			'''
			self.costs.append(current_position.cost)
			self.depths.append(current_position.depth)

			self.evaluate(current_position, func=func)

			try:
				current_position = self.open_list[0]
				del self.open_list[0]
			except:
				print('\nNO SOLUTIONS FOUND - OPEN LIST EMPTY\n')
				self.overall_time = -1
				break

			self.searches += 1

			if(self.searches == self.max_searches):
				print('NO SOLUTIONS FOUND - MAX SEARCHES REACHED')
				self.overall_time = -2
				break

class AStar(Search):

	def __init__(self, max_searches=15000, outfile=None):
		Search.__init__(self, max_searches=max_searches, outfile=outfile)
		self.closed_list = pd.DataFrame()

	def evaluate(self, current_position, func):
		children = self.build_children(current_position, func=func)
		self.open_list = children + self.open_list
		costs = [node.cost for node in self.open_list]
		idc = np.argsort(costs)
		self.open_list = np.array(self.open_list)[idc].tolist()

class BestFirst(Search):

	def __init__(self, max_searches=15000, outfile=None):
		Search.__init__(self, max_searches=max_searches, outfile=outfile)

	def evaluate(self, current_position, func):

		self.closed_list = self.closed_list.append({'State' : str(list(current_position.state))}, 
													   ignore_index=True)
		children = self.build_children(current_position, func=func)
		self.open_list = children + self.open_list
		costs = [node.cost for node in self.open_list]
		idc = np.argsort(costs)
		self.open_list = np.array(self.open_list)[idc].tolist()

