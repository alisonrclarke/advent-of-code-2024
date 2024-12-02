import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day02_test_input{suffix}.txt"
else:
    input_file = f"day02_input.txt"

data = utils.input_as_lines(input_file)

safe_count = 0
for line in data:
    levels = [int(s) for s in line.split()]
    all_inc = all(levels[i] < levels[i + 1] for i in range(len(levels) - 1))
    all_dec = all(levels[i] > levels[i + 1] for i in range(len(levels) - 1))

    if all_inc or all_dec:
        safe = all(abs(levels[i] - levels[i + 1]) < 4 for i in range(len(levels) - 1))
        if safe:
            safe_count += 1

print(f"Part 1: {safe_count}")

safe_count = 0
for line in data:
    levels = [int(s) for s in line.split()]

    remove_index = 0
    all_levels = levels
    while remove_index <= len(levels) + 1:
        all_inc = all(levels[i] < levels[i + 1] for i in range(len(levels) - 1))
        all_dec = all(levels[i] > levels[i + 1] for i in range(len(levels) - 1))

        if all_inc or all_dec:
            safe = all(
                abs(levels[i] - levels[i + 1]) < 4 for i in range(len(levels) - 1)
            )
            if safe:
                safe_count += 1
                break

        levels = all_levels[:remove_index] + all_levels[remove_index + 1 :]
        remove_index += 1


print(f"Part 2: {safe_count}")
