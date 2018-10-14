import os, sys
sys.path.append('search.py')
sys.path.append('heuristics.py')
from search import DFS, AStar, BestFirst
import heuristics as h
import numpy as np

if __name__ == '__main__':

	puzzle = np.array([int(val) for val in sys.argv[1:13]])

	if(len(puzzle) != 12):
		print('INVALID PUZZLE - LENGTH MUST BE 12')
		sys.exit()

	bfs = DFS(h.h1, max_depth=int(sys.argv[13]) if len(sys.argv) >= 13 else None,
			  iter_deep=int(sys.argv[14]) if len(sys.argv) >= 14 else None,
			  outfile='Data/Results/puzzleDFS.txt')
	bfs.traversal(puzzle, verbose=0)

	for heur_str, func in zip(['h1', 'h2'], [h.h1, h.h2]):

		bf = BestFirst(outfile='Data/Results/puzzleBFS-%s.txt' % heur_str)
		bf.traversal(puzzle, func, verbose=0)

		aS = AStar(outfile='Data/Results/puzzleAs-%s.txt' % heur_str)
		aS.traversal(puzzle, func, verbose=0)