import sys
from collections import defaultdict

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day20_test_input{suffix}.txt"
else:
    input_file = f"day20_input.txt"

grid = utils.input_as_lines(input_file)


def get_grid(c: complex):
    return grid[int(c.imag)][int(c.real)]


# Find start and end positions
start_pos = None
end_pos = None
for j, row in enumerate(grid):
    for i, c in enumerate(row):
        if c == "S":
            start_pos = complex(i, j)
        elif c == "E":
            end_pos = complex(i, j)
    if start_pos and end_pos:
        break

# Find the main path through the maze
current = start_pos
path = [current]
while True:
    if current == end_pos:
        break

    for step in (1, -1, 1j, -1j):
        next_pos = current + step
        if next_pos not in path and get_grid(next_pos) in (".", "E"):
            path.append(next_pos)
            current = next_pos
            break

path_length = len(path) - 1

total = 0

for i, pos in enumerate(path[:-1]):
    # Can we walk through a wall and reach an empty space?
    for step in (1, -1, 1j, -1j):
        cheat_start = pos + step
        cheat_end = cheat_start + step
        if cheat_start not in path and cheat_end in path[i:]:
            cheat_end_index = path.index(cheat_end)
            shortcut_length = cheat_end_index - i - 2  # the shortcut takes 2 steps
            if shortcut_length >= 100:
                total += 1

print(f"Part 1: {total}")

# Part 2
total = 0
# cheat_counts - use to check against test data but commented out for the real thing
# cheat_counts = defaultdict(lambda: 0)

print(f"Iterating over {len(path)} path steps")
for i, pos in enumerate(path[:-1]):
    # Iterate over possible cheat paths up to 6 steps
    for j in range(2, 21):
        # Squares reachable in j steps are those with manhattan grid distance of j
        # So need to iterate over possible pairs adding up to j, and try those vals in each direction
        for k in range(j):
            horiz_steps = k
            vert_steps = j - k

            for direction in (1, -1, 1j, -1j):
                step = direction * complex(horiz_steps, vert_steps)
                cheat_end = pos + step
                if cheat_end in path[i:]:
                    cheat_end_index = path.index(cheat_end)
                    shortcut_length = cheat_end_index - i - j
                    # cheat_counts[shortcut_length] += 1
                    if shortcut_length >= (50 if test_mode else 100):
                        total += 1

    if i % 10 == 0:
        print(i)

print(f"Part 2: {total}")
# for k in sorted(cheat_counts.keys()):
#     print(k, cheat_counts[k])
