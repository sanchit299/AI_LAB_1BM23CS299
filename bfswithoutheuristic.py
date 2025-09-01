from collections import deque

# Goal state for the 8 puzzle
goal_state = '123804765'  # Using '0' as the empty tile

# Moves: U, D, L, R (Up, Down, Left, Right)
moves = {
    'U': -3,
    'D': 3,
    'L': -1,
    'R': 1
}

# Valid moves for each index to prevent wrapping around rows/columns
invalid_moves = {
    0: ['U', 'L'], 1: ['U'], 2: ['U', 'R'],
    3: ['L'],        5: ['R'],
    6: ['D', 'L'], 7: ['D'], 8: ['D', 'R']
}

# Function to generate new puzzle state after moving the blank
def move_tile(state, direction):
    index = state.index('0')
    if direction in invalid_moves.get(index, []):
        return None

    new_index = index + moves[direction]
    if new_index < 0 or new_index >= 9:
        return None

    state_list = list(state)
    # Swap 0 with the target tile
    state_list[index], state_list[new_index] = state_list[new_index], state_list[index]
    return ''.join(state_list)

# Helper function to print the state in 3x3 format
def print_state(state):
    for i in range(0, 9, 3):
        # Replace '0' with space for readability
        print(' '.join(state[i:i+3]).replace('0', ' '))
    print()  # Blank line for spacing

# BFS Algorithm with printing all visited states
def bfs(start_state):
    visited = set()
    queue = deque([(start_state, [])])  # Each element is (state, path)

    while queue:
        current_state, path = queue.popleft()

        if current_state in visited:
            continue

        # Print each visited state
        print("Visited state:")
        print_state(current_state)

        if current_state == goal_state:
            return path

        visited.add(current_state)

        for direction in moves:
            new_state = move_tile(current_state, direction)
            if new_state and new_state not in visited:
                queue.append((new_state, path + [direction]))

    return None  # No solution found

# Input initial state as a string (e.g., '123456780' where 0 is the blank)
start = input("Enter start state (e.g., 724506831): ")

if len(start) == 9 and set(start) == set('012345678'):
    print("Start state:")
    print_state(start)
    
    result = bfs(start)
    
    if result is not None:
        print("Solution found!")
        print("Moves:", ' '.join(result))
        print("Number of moves:", len(result))
        print("1BM23CS299\n")
        print("Sanchit Mehta")

        # Print puzzle states after each move in solution path
        current_state = start
        for i, move in enumerate(result, 1):
            current_state = move_tile(current_state, move)
            print(f"Move {i}: {move}")
            print_state(current_state)
    else:
        print("No solution exists for the given start state.")
else:
    print("Invalid input! Please enter a 9-digit string using digits 0-8 without repetition.")