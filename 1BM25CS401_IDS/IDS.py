def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()


def get_moves(state):
    moves = []

    zero = state.index(0)
    row, col = divmod(zero, 3)

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    for dr, dc in directions:
        r = row + dr
        c = col + dc

        if 0 <= r < 3 and 0 <= c < 3:
            new_state = list(state)
            pos = r * 3 + c

            new_state[zero], new_state[pos] = \
                new_state[pos], new_state[zero]

            moves.append(tuple(new_state))

    return moves


def depth_limited_search(state, goal, limit, path):

    if state == goal:
        return path

    if limit == 0:
        return None

    for next_state in get_moves(state):

        if next_state not in path:

            result = depth_limited_search(
                next_state,
                goal,
                limit - 1,
                path + [next_state]
            )

            if result is not None:
                return result

    return None


def ids(initial, goal):

    depth = 0

    while True:

        solution = depth_limited_search(
            initial,
            goal,
            depth,
            [initial]
        )

        if solution is not None:
            return solution

        depth += 1


initial = (
    1, 2, 3,
    4, 0, 6,
    7, 5, 8
)

goal = (
    1, 2, 3,
    4, 5, 6,
    7, 8, 0
)

solution = ids(initial, goal)

print("Solution:")

for state in solution:
    print_state(state)