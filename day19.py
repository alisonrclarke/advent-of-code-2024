import sys
from functools import cache

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day19_test_input{suffix}.txt"
else:
    input_file = f"day19_input.txt"

data = utils.input_as_lines(input_file)

towels = data[0].split(", ")


@cache
def can_make_pattern(pattern):
    if pattern in towels:
        return True

    start_towels = [t for t in towels if pattern.startswith(t)]
    return any(can_make_pattern(pattern[len(t) :]) for t in start_towels)


possible_patterns = []

for line in data[2:]:
    if can_make_pattern(line):
        possible_patterns.append(line)


print(f"Part 1: {len(possible_patterns)}")


@cache
def pattern_possibilities(pattern):
    total = 0
    options = set()
    if pattern in towels:
        total += 1
        options.add((pattern,))

    start_towels = [t for t in towels if pattern.startswith(t) and pattern != t]
    n_tail_options = [pattern_possibilities(pattern[len(t) :]) for t in start_towels]
    return total + sum(n_tail_options)


total = 0
for pattern in possible_patterns:
    n_options = pattern_possibilities(pattern)
    total += n_options

print(f"Part 2: {total}")
