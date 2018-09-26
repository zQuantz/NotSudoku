import os, sys
sys.path.append('search.py')
sys.path.append('heuristics.py')
from search import BFS, AStar, BestFirst
import heuristics as h
import numpy as np
from argparse import ArgumentParser

if __name__ == '__main__':

	parser = ArgumentParser(description='An API to find solutions for the 11-d Puzzle.')
	parser.add_argument('-p','--puzzle', action='append', help='<Required> Set flag', required=True)
	parser.add_argument('-md', '--max_depth', default=5, type=int)
	args = parser.parse_args()
	puzzle = eval(args.puzzle[0])

	if(len(puzzle) != 12):
		print('INVALID PUZZLE - LENGTH MUST BE 12')
		sys.exit()

	#bfs = BFS(np.array(puzzle), h.h1, max_depth=args.max_depth, outfile='Data/Results/puzzleDFS.txt')
	#bfs.traversal()

	for heur_str, func in zip(['h1', 'h2'], [h.h3, h.h2]):

		bf = BestFirst(outfile='Data/Results/puzzleBFS-%s.txt' % heur_str)
		bf.traversal(np.array(puzzle), func)

		aS = AStar(outfile='Data/Results/puzzleAs-%s.txt' % heur_str)
		aS.traversal(np.array(puzzle), func)