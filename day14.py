from collections import defaultdict
from functools import reduce
import operator
import os
import re
import sys
from time import sleep

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day14_test_input{suffix}.txt"
else:
    input_file = f"day14_input.txt"


data = utils.input_as_lines(input_file)

end_quadrants = defaultdict(lambda: 0)

if test_mode:
    width = 11
    height = 7
else:
    width = 101
    height = 103

for line in data:
    matches = [int(n) for n in re.findall(r"-?\d+", line)]
    pos = (matches[0], matches[1])
    v = (matches[2], matches[3])

    end_x = (pos[0] + v[0] * 100) % width
    end_y = (pos[1] + v[1] * 100) % height

    quadrant_x = None
    quadrant_y = None

    if end_x < width // 2:
        quadrant_x = 0
    elif end_x >= (width + 1) // 2:
        quadrant_x = 1

    if end_y < height // 2:
        quadrant_y = 0
    elif end_y >= (height + 1) // 2:
        quadrant_y = 1

    if quadrant_x is not None and quadrant_y is not None:
        end_quadrants[(quadrant_x, quadrant_y)] += 1

print(end_quadrants)
total = reduce(operator.mul, end_quadrants.values(), 1)
print(f"Part 1: {total}")


# Part 2 - draw some pictures!
bots = []
bot_map = defaultdict(lambda: 0)
for line in data:
    matches = [int(n) for n in re.findall(r"-?\d+", line)]
    pos = (matches[0], matches[1])
    v = (matches[2], matches[3])

    bots.append((pos, v))
    bot_map[pos] += 1

iterations = 0

while iterations < 10000:
    next_bots = []
    bot_map = defaultdict(lambda: 0)

    for pos, v in bots:
        end_x = (pos[0] + v[0]) % width
        end_y = (pos[1] + v[1]) % height
        next_bots.append(((end_x, end_y), v))
        bot_map[(end_x, end_y)] += 1

    bots = next_bots
    iterations += 1

    # Figure out how it would look printed out, and see whether or not it might look like a tree
    possible_tree = False
    map_as_string = ""

    for j in range(height):
        line = ""
        for i in range(width):
            n = bot_map[(i, j)]
            if n > 0:
                line += "X"
            else:
                line += " "

        # Look for a row of Xs that might make up the bottom of the tree or something
        if "XXXXXXXXXX" in line:
            possible_tree = True

        map_as_string += line + "\n"

    if possible_tree:
        print()
        print(map_as_string)
        print()
        print(f"Iteration {iterations}")
        print("Is this a Christmas tree? y/N:")

        if input().lower() == "y":
            break

    if iterations % 100 == 0:
        print(f"Completed {iterations} iterations")


print(f"Part 2: {iterations}")
