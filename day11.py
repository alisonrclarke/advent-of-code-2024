from functools import cache
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day11_test_input{suffix}.txt"
else:
    input_file = f"day11_input.txt"

data = utils.input_as_string(input_file)


@cache
def step(n):
    if n == 0:
        return [1]
    elif len(str(n)) % 2 == 0:
        str_len = len(str(n)) // 2
        return [int(str(n)[:str_len]), int(str(n)[str_len:])]
    else:
        return [n * 2024]


current = [int(s) for s in data.split()]

for i in range(25):
    next_ = []
    for s in current:
        next_.extend(step(s))
    current = next_

print(f"Part 1: {len(current)}")


# Part 2 - need to be more efficient, so cache the total for a value and number of steps
@cache
def n_stones(s, n_steps):
    if n_steps == 0:
        return 1
    else:
        return sum([n_stones(s2, n_steps - 1) for s2 in step(s)])


current = [int(s) for s in data.split()]
total = 0
for s in current:
    total += n_stones(s, 75)

print(f"Part 2: {total}")
