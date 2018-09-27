import numpy as np
import sys, os
sys.path.append('search.py')
sys.path.append('heuristics.py')
from search import BFS, BestFirst, AStar
import heuristics as h

if __name__ == '__main__':

	state = np.load('Data/states.npy')[2]

	bf = BestFirst()
	bf.traversal(state, h.O2)