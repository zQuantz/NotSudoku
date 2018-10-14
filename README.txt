To test a puzzle, run "python search_api.py 1 2 3 4 5 6 7 8 9 10 11 0"
where 1 2 .. 0 is the puzzle as specified in the instructions. 

Please run the script inside of the main directory to allow for the saving
of results.

To run DEPTH LIMITED SEARCH, append a single integer corresponding to the
depth cutoff at the end of the puzzle. 

To run ITERATIVE DEEPENING SEARCH, append a single integer corresponding
to the depth cutoff at the end of the puzzle AND a single integer corresponding
to the incrementation of the depth cut off.

-------------------------------------------------

EXAMPLE:

Puzzle
1 2 3 4
5 6 7 8
9 10 11 0

SIMPLE TEST
python search_api.py 1 2 3 4 5 6 7 8 9 10 11 0

DEPTH LIMITED SEARCH
python search_api.py 1 2 3 4 5 6 7 8 9 10 11 0 5

ITERATIVE DEEPENING SEARCH
python search_api.py 1 2 3 4 5 6 7 8 9 10 11 0 5 2

--------------------------------------------------


