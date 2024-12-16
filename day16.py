from functools import cache
import sys

import utils

# It's that time of year...
sys.setrecursionlimit(2000)

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day16_test_input{suffix}.txt"
else:
    input_file = f"day16_input.txt"

grid = utils.input_as_lines(input_file)

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

# @cache
shortest_path_cache = {}


def shortest_path(pos1, pos2, step, visited):
    # print("shortest_path", pos1, pos2, step, visited)

    cache_key = (pos1, pos2, step)
    if cache_key in shortest_path_cache:
        print("cache hit")
        return shortest_path_cache[cache_key]

    if pos1 + step == pos2:
        shortest_path_cache[cache_key] = 1
        return 1
    else:
        possible_scores = []

        next_pos = pos1 + step
        if (
            next_pos not in visited
            and grid[int(next_pos.imag)][int(next_pos.real)] == "."
        ):
            possible_scores.append(
                1 + shortest_path(pos1 + step, pos2, step, visited + [pos1])
            )

        for s in [step * 1j, step * -1j]:
            if pos1 + s == pos2:
                possible_scores += 1001

            next_pos = pos1 + s
            if (
                next_pos not in visited
                and grid[int(next_pos.imag)][int(next_pos.real)] == "."
            ):
                possible_scores.append(
                    1001 + shortest_path(pos1 + s, pos2, s, visited + [pos1])
                )

        if possible_scores:
            score = min(possible_scores)
        else:
            score = sys.maxsize

        shortest_path_cache[cache_key] = score
        return score


part1 = shortest_path(start_pos, end_pos, 1, [])
print(f"Part 1: {part1}")

# Answer too high (338120)
