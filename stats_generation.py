import numpy as np
import pandas as pd
import os, sys
sys.path.append('search.py')
from search import BFS, BestFirst, AStar

if __name__ == '__main__':

	states = np.load('Data/states.npy')
	stats = pd.DataFrame()

	for state in states[:1]:
