import re
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day03_test_input{suffix}.txt"
else:
    input_file = f"day03_input.txt"

data = utils.input_as_string(input_file)

total = 0

for x, y in re.findall(r"mul\((\d+),(\d+)\)", data):
    total += int(x) * int(y)

print(f"Part 1: {total}")

total = 0
do = True

for op, args in re.findall(r"(mul|do|don\'t)\(([\d,]*)\)", data):
    if op == "don't":
        do = False
    elif op == "do":
        do = True
    elif do:
        x, y = args.split(",")
        total += int(x) * int(y)

print(f"Part 2: {total}")
