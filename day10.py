from collections import defaultdict
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day10_test_input{suffix}.txt"
else:
    input_file = f"day10_input.txt"

data = utils.input_as_lines(input_file)

trailheads = []
grid = [[None] * (len(data[0]) + 2)]

for j, line in enumerate(data):
    grid.append([None] + [int(c) for c in line] + [None])
    trailheads.extend([complex(i, j + 1) for i, n in enumerate(grid[j + 1]) if n == 0])

grid.append([None] * (len(data[0]) + 2))


def search(n, pos):
    steps = [1, -1, 1j, -1j]
    next_positions = set()
    for s in steps:
        pos2 = pos + s
        if grid[int(pos2.imag)][int(pos2.real)] == n:
            next_positions.add(pos2)
    return next_positions


total = 0

for pos in trailheads:
    n = 0
    current_positions = {pos}
    for n in range(1, 10):
        next_positions = [search(n, p) for p in current_positions]

        if next_positions:
            current_positions = set.union(*next_positions)
        else:
            current_positions = set()

    total += len(current_positions)

print(f"Part 1: {total}")

# Part 2: use map to get list of possible paths from each pos to the next

possible_paths = defaultdict(set)

for pos in trailheads:
    n = 0
    current_positions = {pos}
    for n in range(1, 10):
        next_positions = [(p, search(n, p)) for p in current_positions]

        current_positions = set()

        for p1, p_next in next_positions:
            for p2 in p_next:
                possible_paths[p1].add(p2)
                current_positions.add(p2)


# Now use the possible paths to determine the number of paths
def get_routes(n, route):
    if n == 9:
        return [route]
    else:
        routes = []
        for p in possible_paths[route[-1]]:
            next_routes = get_routes(n + 1, route + [p])
            routes.extend(next_routes)

        return routes


total = 0
for pos in trailheads:
    routes = get_routes(0, [pos])
    total += len(routes)


print(f"Part 2: {total}")
