import numpy as np
import pandas as pd
import os, sys
sys.path.append('search.py')
from search import BFS_t, BestFirst_t, AStar_t
sys.path.append('heuristics.py')
import heuristics as h

if __name__ == '__main__':

	states = np.load('Data/states.npy')
	diffs = np.load('Data/diffs.npy')
	stats = pd.DataFrame()
	func = h.h2
	func_str = 'h2_p'

	for i, state in enumerate(states[:20]):
		print(i)
		os.makedirs('Data/Stats/%s/state_%d/' % (func_str, i))
		print('Data/Stats/%s/state_%d/' % (func_str, i))
		'''
		## BFS ## 
		bfs = BFS(state, 50, func)
		bfs.traversal()
		df = pd.DataFrame({'Costs' : bfs.costs, 
						   'Depths' : bfs.depths, 
						   'Time' : [bfs.overall_time]*len(bfs.costs), 
						   'HTime' : [np.mean(bfs.heuristic_time)]*len(bfs.costs), 
						   'Searches' : [bfs.searches]*len(bfs.costs), 
						   'Difficulty' : [diff]*len(bfs.costs)})
		df.to_pickle('Data/stats/h2/state_%d/bfs.pkl' % i)
		'''
		##
		## BestFirst ##
		print('BEST FIRSTTTTT')
		bf = BestFirst_t()
		bf.traversal(state, func)
		n = len(bf.costs)
		df = pd.DataFrame({'Costs' : bf.costs, 
						   'Depths' : bf.depths, 
						   'Time' : [bf.overall_time]*n, 
						   'HTime' : [np.mean(bf.heuristic_time)]*n, 
						   'Searches' : [bf.searches]*n, 
						   'Difficulty' : [diffs[i % 4]]*n, 
						   'SolutionLength' : [bf.solution_path_length]*n})
		df.to_pickle('Data/stats/%s/state_%d/bf.pkl' % (func_str, i))
		print(df.head())
		## AStar ##
		print('A STARRRRRRR')
		aS = AStar_t()
		aS.traversal(state, func)
		n = len(aS.costs)
		df = pd.DataFrame({'Costs' : aS.costs, 
						   'Depths' : aS.depths, 
						   'Time' : [aS.overall_time]*n, 
						   'HTime' : [np.mean(aS.heuristic_time)]*n, 
						   'Searches' : [aS.searches]*n, 
						   'Difficulty' : [diffs[i % 4]]*n,
						   'SolutionLength' : [aS.solution_path_length]*n})
		df.to_pickle('Data/stats/%s/state_%d/as.pkl' % (func_str,i))
		print(df.head())
		##
