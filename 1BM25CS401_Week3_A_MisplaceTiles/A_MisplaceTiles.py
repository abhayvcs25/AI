import heapq

# Define the global goal state (0 represents the blank tile)
GOAL_STATE = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)

# Valid movement shifts for the blank tile (row_offset, col_offset, label)
MOVES = [(-1, 0, 'Up'), (1, 0, 'Down'), (0, -1, 'Left'), (0, 1, 'Right')]

def get_neighbors(state):
    """Finds all legal board layouts achievable by moving the blank space."""
    neighbors = []
    blank_idx = state.index(0)
    r, c = divmod(blank_idx, 3)

    for dr, dc, move_name in MOVES:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            neighbor_idx = nr * 3 + nc
            new_state = list(state)
            # Swap the blank tile with the target tile
            new_state[blank_idx], new_state[neighbor_idx] = new_state[neighbor_idx], new_state[blank_idx]
            neighbors.append((tuple(new_state), move_name))

    return neighbors

def h_misplaced_tiles(state):
    """Heuristic function: Counts tiles that are not in their goal position."""
    count = 0
    for i in range(9):
        # Do not count the blank tile (0) as a misplaced tile
        if state[i] != 0 and state[i] != GOAL_STATE[i]:
            count += 1
    return count

def a_star_misplaced(start_state):
    """Executes A* Search using Misplaced Tiles heuristic.
    Returns the path of states, path of moves, and g_score.
    """
    # Priority Queue elements format: (f_score, g_score, current_layout, state_history, move_history)
    h_start = h_misplaced_tiles(start_state)
    pq = [(h_start, 0, start_state, [start_state], [])]

    # Tracking visited states to optimize and prevent cycles
    visited = {start_state: 0}

    while pq:
        f, g, current, state_path, move_path = heapq.heappop(pq)

        if current == GOAL_STATE:
            return state_path, move_path, g

        for neighbor, move in get_neighbors(current):
            new_g = g + 1
            if neighbor not in visited or new_g < visited[neighbor]:
                visited[neighbor] = new_g
                h = h_misplaced_tiles(neighbor)
                new_f = new_g + h
                heapq.heappush(pq, (new_f, new_g, neighbor, state_path + [neighbor], move_path + [move]))

    return None, None, -1

def print_grid(state):
    """Prints the 3x3 layout of a given state."""
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

if __name__ == "__main__":
    # Supply your initial layout configuration here
    initial_state = (1, 2, 3,
                     0, 4, 6,
                     7, 5, 8)

    print("--- A* Search: Misplaced Tiles Heuristic ---")
    print(f"Initial Configuration: {initial_state}\n")

    state_path, move_path, total_depth = a_star_misplaced(initial_state)

    if state_path is not None:
        print(f"Goal reached at depth (g): {total_depth}\n")
        print("--- Sequence of States ---")
        print("Step 0 (Initial State):")
        print_grid(state_path[0])

        for idx in range(1, len(state_path)):
            print(f"Step {idx} (Move: {move_path[idx-1]}):")
            print_grid(state_path[idx])
    else:
        print("No viable solution sequence found.")