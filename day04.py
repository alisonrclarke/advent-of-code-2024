import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day04_test_input{suffix}.txt"
else:
    input_file = f"day04_input.txt"

lines = utils.input_as_lines(input_file)

# Expand the grid so we don't need to worry about edge cases
grid = ["." * (len(lines[0]) + 6)] * 3
grid += ["..." + line + "..." for line in lines]
grid += ["." * (len(lines[0]) + 6)] * 3

total = 0

for y in range(3, len(lines) + 3):
    for x in range(3, len(lines[0]) + 3):
        if grid[y][x] == "X":
            x_pos = complex(x, y)
            # Look in all positions around to find M
            for y2 in (-1, 0, 1):
                for x2 in (-1, 0, 1):
                    if grid[y + y2][x + x2] == "M":
                        # Now we have the m position, get the vector from the X and use to check for A and S
                        m_pos = complex(x + x2, y + y2)
                        diff = m_pos - x_pos
                        a_pos = m_pos + diff
                        if grid[int(a_pos.imag)][int(a_pos.real)] == "A":
                            s_pos = a_pos + diff
                            if grid[int(s_pos.imag)][int(s_pos.real)] == "S":
                                total += 1

print(f"Part 1: {total}")

# Part 2
total = 0

# Use original lines as we're looking for As in the middle so no worry re: edge cases if we start at index 1
for y in range(1, len(lines) - 1):
    for x in range(1, len(lines[0]) - 1):
        if lines[y][x] == "A":
            if (
                (lines[y - 1][x - 1] == "M" and lines[y + 1][x + 1] == "S")
                or (lines[y - 1][x - 1] == "S" and lines[y + 1][x + 1] == "M")
            ) and (
                (lines[y + 1][x - 1] == "M" and lines[y - 1][x + 1] == "S")
                or (lines[y + 1][x - 1] == "S" and lines[y - 1][x + 1] == "M")
            ):
                total += 1


print(f"Part 2: {total}")
