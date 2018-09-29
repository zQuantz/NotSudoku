import numpy as np
import pandas as pd
import os, sys
sys.path.append('search.py')
from search import BFS, BestFirst, AStar
sys.path.append('heuristics.py')
import heuristics as h

if __name__ == '__main__':

	if(True):

		states = np.load('Data/states_bfs.npy')
		diffs = np.load('Data/diffs_bfs.npy')
		max_searches=10000000

		for i, state in enumerate(states):
			## BFS ##
			bfs = BFS(max_searches=max_searches, iter_deep=2, max_depth=3)
			bfs.traversal(state, func=None, verbose=1)
			df = pd.DataFrame(bfs.iter_deep_stats, columns = ['NumNodes', 'Depth', 'Searches'])
			df['Time'] = [bfs.overall_time]*len(df)
			df['Searches'] = [bfs.searches]*len(df)
			df['Difficulty'] = [diffs[i % len(diffs)]]*len(df)
			df['SolutionLength'] = [bfs.solution_path_length]*len(df)
			df.to_pickle('Data/Stats/bfs/state_%d.pkl' % i)
			##
	else:

		states = np.load('Data/states.npy')
		diffs = np.load('Data/diffs.npy')
		max_searches=15000

		for func, func_str in zip([h.h1, h.h2, h.h3, 
								   h.h4][3:] ,
								   ['h1', 'h2', 'h3', 
								    'h4'][3:]):

			for i, state in enumerate(states):
				print(i)
				os.makedirs('Data/Stats/%s/state_%d/' % (func_str, i))
				print('Data/Stats/%s/state_%d/' % (func_str, i))
				
				## BestFirst ##
				bf = BestFirst(max_searches=max_searches)
				bf.traversal(state, func)
				n = len(bf.costs)
				df = pd.DataFrame({'Costs' : bf.costs, 
								   'Depths' : bf.depths, 
								   'Time' : [bf.overall_time]*n, 
								   'HTime' : [np.mean(bf.heuristic_time)]*n, 
								   'Searches' : [bf.searches]*n, 
								   'Difficulty' : [diffs[i % len(diffs)]]*n, 
								   'SolutionLength' : [bf.solution_path_length]*n})
				df.to_pickle('Data/Stats/%s/state_%d/bf.pkl' % (func_str, i))
				## AStar ##
				aS = AStar(max_searches=max_searches)
				aS.traversal(state, func)
				n = len(aS.costs)
				df = pd.DataFrame({'Costs' : aS.costs,
								   'Depths' : aS.depths,
								   'Time' : [aS.overall_time]*n,
								   'HTime' : [np.mean(aS.heuristic_time)]*n,
								   'Searches' : [aS.searches]*n,
								   'Difficulty' : [diffs[i % len(diffs)]]*n,
								   'SolutionLength' : [aS.solution_path_length]*n})
				df.to_pickle('Data/Stats/%s/state_%d/as.pkl' % (func_str,i))
				##
