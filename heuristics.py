import numpy as np
### HEURISTICS ### 

def h1(board_state):
	goal_state = np.append(np.arange(1, 12), 0)
	return 12 - np.where(goal_state == board_state)[0].shape[0]

def h1_mod(board_state):
    board_state = board_state.tolist()
    cost = [abs(board_state.index(i) - i + 1) for i in range(1, 12)]
    cost = cost + [abs(11 - board_state.index(0))]
    return sum(cost)

def h2(board_state):
    board_state = board_state.reshape(3, 4)
    goal_state = np.append(np.arange(1, 12), 0).reshape(3, 4)
    cost = 0
    for i in goal_state.ravel():
        idx_board = np.argwhere(board_state==i)[0]
        idx_goal = np.argwhere(goal_state==i)[0]
        cost += sum(abs(idx_board - idx_goal))
    return cost

def h2_mod(board_state):
    board_state = board_state.reshape(3, 4)
    goal_state = np.append(np.arange(1, 12), 0).reshape(3, 4)
    cost = 0
    for i in goal_state.ravel():
        idx_board = np.argwhere(board_state==i)[0]
        idx_goal = np.argwhere(goal_state==i)[0]
        cost += max(abs(idx_board - idx_goal))
    return cost

def h3(board_state):
    goal_state = np.append(np.arange(1, 12), 0).reshape(3, 4)
    board_state = board_state.reshape(3, 4)
    goal_sum = np.append(goal_state.sum(axis=0)/3, goal_state.sum(axis=1)/4)
    board_sum = np.append(board_state.sum(axis=0)/3, board_state.sum(axis=1)/4)
    return np.sqrt(np.sum(np.power(board_sum - goal_sum, 2)))

def O2(board_state):
    l1_cost = h2(board_state)
    moves = get_legal_moves(board_state)
    l2_cost = min([h2(move[0]) for move in moves])
    return l1_cost+l2_cost

###