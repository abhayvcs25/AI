import random

def calculate_attacks(state):
    n = len(state)
    attacks = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks

def get_best_neighbor(state):
    n = len(state)
    current_h = calculate_attacks(state)
    best_neighbors = []
    best_h = float('inf')  # Fix: Track the lowest cost found *among neighbors*

    for col in range(n):
        for row in range(n):
            if state[col] == row:
                continue
            neighbor = list(state)
            neighbor[col] = row
            h = calculate_attacks(neighbor)

            print_board(neighbor)
            print("cost = ",h)

            if h < best_h:
                best_h = h
                best_neighbors = [neighbor]
            elif h == best_h:
                best_neighbors.append(neighbor)

    # Fix: If the best neighbor found isn't better than current state,
    # return the current state to signal we hit a peak or plateau
    if best_h < current_h:
        return random.choice(best_neighbors), best_h
    return state, current_h


def hill_climbing_search(n, max_restarts=100):
    print(f"Solving {n}-Queens using Hill Climbing...\n")
    for attempt in range(1, max_restarts + 1):
        initial_state = [random.randint(0, n - 1) for _ in range(n)]
        state = list(initial_state)
        current_h = calculate_attacks(state)

        while True:

            neighbor, neighbor_h = get_best_neighbor(state)
            if neighbor_h >= current_h:
                break
            print("\n=======Selected=======")
            print_board(neighbor)
            print("cost = ",neighbor_h)
            print("======================\n")
            state = neighbor
            current_h = neighbor_h

        if current_h == 0:
            print("\n--- GOAL STATE ---")
            print_board(state)
            return state

    print(f"Could not find a solution within {max_restarts} restarts.")
    return None

def print_board(state):
    n = len(state)
    for row in range(n):
        line = ""
        for col in range(n):
            if state[col] == row:
                line += " Q "
            else:
                line += " . "
        print(line)
    print(f"State: {state}")


Queens=int(input("Enter the number of Queens = "))
solution = hill_climbing_search(Queens)