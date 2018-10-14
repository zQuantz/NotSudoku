import numpy as np
import pandas as pd
import os, sys
sys.path.append('search.py')
from search import DFS, BestFirst, AStar
sys.path.append('heuristics.py')
import heuristics as h

if __name__ == '__main__':

	if(True):

		states = np.load('Data/states_bfs.npy')
		diffs = np.load('Data/diffs_bfs.npy')
		max_searches=10000000

		for i, state in enumerate(states):
			## BFS ##
			dfs = DFS(max_searches=max_searches, iter_deep=2, max_depth=3)
			dfs.traversal(state, func=None, verbose=0)
			df = pd.DataFrame(dfs.iter_deep_stats, columns = ['NumNodes', 'Depth', 'Searches'])
			df['Time'] = [dfs.overall_time]*len(df)
			df['Searches'] = [dfs.searches]*len(df)
			df['Difficulty'] = [diffs[i % len(diffs)]]*len(df)
			df['SolutionLength'] = [dfs.solution_path_length]*len(df)
			df.to_pickle('Data/Stats/bfs/state_%d.pkl' % i)
			##
	else:

		states = np.load('Data/states.npy')
		diffs = np.load('Data/diffs.npy')
		max_searches=15000

		for func, func_str in zip([h.h2, h.h3], ['h2_aug', 'h3_aug']):

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
