import copy
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day06_test_input{suffix}.txt"
else:
    input_file = f"day06_input.txt"

grid = utils.input_as_lines(input_file)

# Find start pos
for j, row in enumerate(grid):
    i = row.find("^")
    if i > -1:
        start_pos = complex(i, j)
        break

pos = start_pos
step = -1j
visited = {pos}

while True:
    next_pos = pos + step
    if grid[int(next_pos.imag)][int(next_pos.real)] == "#":
        # Change direction: multipling by i should rotate 90 degrees
        step = step * 1j
    elif (
        next_pos.imag == 0
        or next_pos.imag == len(grid) - 1
        or next_pos.real == 0
        or next_pos.real == len(grid[0]) - 1
    ):
        visited.add(next_pos)
        break
    else:
        visited.add(next_pos)
        pos = next_pos

print(f"Part 1: {len(visited)}")


# Part 2: look for loops :'(


def check_for_loop(grid, start_pos):
    pos = start_pos
    step = -1j
    visited = {pos}
    is_loop = False

    while True:
        next_pos = pos + step
        if (next_pos, step) in visited:
            # We've been here before (from same direction)
            is_loop = True
            break
        if grid[int(next_pos.imag)][int(next_pos.real)] == "#":
            # Change direction: multipling by i should rotate 90 degrees
            step = step * 1j
        elif (
            next_pos.imag == 0
            or next_pos.imag == len(grid) - 1
            or next_pos.real == 0
            or next_pos.real == len(grid[0]) - 1
        ):
            visited.add((next_pos, step))
            break
        else:
            visited.add((next_pos, step))
            pos = next_pos

    return is_loop


# Need to try putting obstacle somewhere guard would visit anyway, so loop through visited
total = 0
for obstacle_pos in visited:
    new_grid = copy.deepcopy(grid)
    row = int(obstacle_pos.imag)
    col = int(obstacle_pos.real)
    new_grid[row] = new_grid[row][:col] + "#" + new_grid[row][col + 1 :]

    is_loop = check_for_loop(new_grid, start_pos)
    if is_loop:
        total += 1

print(f"Part 2: {total}")
