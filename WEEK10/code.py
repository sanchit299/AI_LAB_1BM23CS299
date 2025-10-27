import math

def alpha_beta_search(state):
    return max_value(state, -math.inf, math.inf)

def max_value(state, alpha, beta):
    if terminal_test(state):
        return utility(state)
    v = -math.inf
    for a in actions(state):
        v = max(v, min_value(result(state, a), alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def min_value(state, alpha, beta):
    if terminal_test(state):
        return utility(state)
    v = math.inf
    for a in actions(state):
        v = min(v, max_value(result(state, a), alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

values = [3, 5, 6, 9, 1, 2, 0, -1]
max_depth = 3

def terminal_test(state):
    return state >= len(values) // 2**(max_depth - depth[state])

def utility(state):
    return values[state]

def actions(state):
    if depth[state] == max_depth:
        return []
    return [0, 1]

def result(state, action):
    child = state * 2 + 1 + action
    depth[child] = depth[state] + 1
    return child

depth = {0: 0}
print("Optimal value:", alpha_beta_search(0))
print("Sanchit Mehta")
