import math

def alpha_beta(node, depth, alpha, beta, maximizingPlayer, game_tree):
    """
    Alpha-Beta pruning search algorithm
    node: current node in game tree
    depth: current depth
    alpha: best value for maximizer
    beta: best value for minimizer
    maximizingPlayer: True if maximizer's turn
    game_tree: dictionary representing tree {node: children or value}
    """
    # If leaf node or depth 0, return its value
    if depth == 0 or isinstance(game_tree[node], int):
        return game_tree[node]

    if maximizingPlayer:
        maxEval = -math.inf
        for child in game_tree[node]:
            eval = alpha_beta(child, depth-1, alpha, beta, False, game_tree)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cut-off
        return maxEval
    else:
        minEval = math.inf
        for child in game_tree[node]:
            eval = alpha_beta(child, depth-1, alpha, beta, True, game_tree)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cut-off
        return minEval

# Example game tree
game_tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': 3,
    'E': 5,
    'F': 2,
    'G': 9
}

best_value = alpha_beta('A', depth=3, alpha=-math.inf, beta=math.inf, maximizingPlayer=True, game_tree=game_tree)
print("Best value for maximizer:", best_value)
print("Sanchit Mehta 1bm23cs299")
