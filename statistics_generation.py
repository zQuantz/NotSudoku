import numpy as np
import pandas as pd
import os, sys
sys.path.append('search.py')
from search import BFS, BestFirst, AStar
sys.path.append('heuristics.py')
import heuristics as h

if __name__ == '__main__':

	states = np.load('Data/states.npy')
	diffs = np.load('Data/diffs.npy')
	stats = pd.DataFrame()
	max_searches=15000

	for func, func_str in zip([h.h1, h.h2, h.h3, 
							   h.h1_mod, h.h2_mod, h.h4] ,
							   ['h1', 'h2', 'h3', 
							   'h1_mod', 'h2_mod', 'h4']):

		for i, state in enumerate(states):
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
			##
			'''
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
