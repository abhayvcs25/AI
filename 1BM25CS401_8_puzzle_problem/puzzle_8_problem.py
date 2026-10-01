    
def print_board(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

def get_neighbors(state):
    neighbors = []
    zero_idx = state.index(0)
    row, col = divmod(zero_idx, 3)
    
    directions = [
        (-1, 0, 'Down'),
        (1, 0, 'Up'),
        (0, -1, 'Right'),
        (0, 1, 'Left')
    ]
    
    for dr, dc, direction in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            neighbor_idx = nr * 3 + nc
            tile_moved = state[neighbor_idx]
            new_state = list(state)
            new_state[zero_idx], new_state[neighbor_idx] = new_state[neighbor_idx], new_state[zero_idx]
            neighbors.append((tuple(new_state), f"Tile {tile_moved} moved {direction}"))
            
    return neighbors

def dfs_solve(start, goal, max_depth=50):
    stack = [(start, [start], [])]
    visited = {start: 0}

    while stack:
        state, path, moves = stack.pop()
        
        if state == goal:
            return path, moves
            
        if len(path) > max_depth:
            continue
            
        for neighbor, move_desc in get_neighbors(state):
            if neighbor not in visited or len(path) < visited[neighbor]:
                visited[neighbor] = len(path)
                stack.append((neighbor, path + [neighbor], moves + [move_desc]))
                
    return None, None

initial_state = (1, 2, 3,
           4, 0, 6,
           7, 5, 8)

goal_state = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)

print("Searching for a solution...")
solution_path, moves_taken = dfs_solve(initial_state, goal_state, max_depth=20)

if solution_path:
    print(f"Solution found in {len(solution_path) - 1} moves:\n")
    print("Step 0: Initial State")
    print_board(solution_path[0])
    for step in range(1, len(solution_path)):
        print(f"Step {step} ({moves_taken[step-1]}):")
        print_board(solution_path[step])
else:
    print("No solution found within the specified depth limit.")