from collections import defaultdict
import itertools
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day08_test_input{suffix}.txt"
else:
    input_file = f"day08_input.txt"

data = utils.input_as_lines(input_file)

antennae = defaultdict(list)

for i, line in enumerate(data):
    for j, c in enumerate(line):
        if c != ".":
            antennae[c].append(complex(i, j))

antinodes = set()

for c, positions in antennae.items():
    for p1, p2 in itertools.combinations(positions, 2):
        diff = p2 - p1
        for pos in (p1 - diff, p2 + diff):
            if (
                pos.real >= 0
                and pos.real < len(data[0])
                and pos.imag >= 0
                and pos.imag < len(data)
            ):
                antinodes.add(pos)

print(f"Part 1: {len(antinodes)}")

# Part 2
# For each diff, find simplest fraction between x and y? Or just keep using diff?
antinodes = set()
for c, positions in antennae.items():
    for p1, p2 in itertools.combinations(positions, 2):
        antinodes.add(p1)
        antinodes.add(p2)

        diff = p2 - p1
        pos = p1 - diff
        while (
            pos.real >= 0
            and pos.real < len(data[0])
            and pos.imag >= 0
            and pos.imag < len(data)
        ):
            antinodes.add(pos)
            pos = pos - diff

        pos = p2 + diff
        while (
            pos.real >= 0
            and pos.real < len(data[0])
            and pos.imag >= 0
            and pos.imag < len(data)
        ):
            antinodes.add(pos)
            pos = pos + diff

for i, line in enumerate(data):
    for j, c in enumerate(line):
        if complex(i, j) in antinodes:
            print("#", end="")
        else:
            print(c, end="")
    print()


print(f"Part 2: {len(antinodes)}")
