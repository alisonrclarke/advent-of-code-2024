import operator
import re
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ''
    input_file = f'day01_test_input{suffix}.txt'
else:
    input_file = f'day01_input.txt'

data = utils.input_as_lines(input_file)

left = []
right = []

for line in data:
    l, r = re.split(r'\s+', line)
    left.append(int(l))
    right.append(int(r))

left.sort()
right.sort()

total = 0
for i in range(len(left)):
    total += abs(left[i] - right[i])

print(f"Part 1: {total}")

total = 0
for i in left:
    n = operator.countOf(right, i)
    total += i * n

print(f"Part 2: {total}")