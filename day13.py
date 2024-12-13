import math
import re
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day13_test_input{suffix}.txt"
else:
    input_file = f"day13_input.txt"

data = utils.input_as_lines(input_file)

i = 0
button_re = re.compile(r"Button \w: X\+(\d+), Y\+(\d+)")
prize_re = re.compile(r"Prize: X=(\d+), Y=(\d+)")
total = 0
total2 = 0

while i < len(data):
    a_match = button_re.match(data[i])
    a_move = complex(int(a_match.group(1)), int(a_match.group(2)))

    b_match = button_re.match(data[i + 1])
    b_move = complex(int(b_match.group(1)), int(b_match.group(2)))

    prize_match = prize_re.match(data[i + 2])
    prize_pos = complex(int(prize_match.group(1)), int(prize_match.group(2)))

    # Part 1 (initial solution) - brute force
    min_cost = None

    for a in range(100):
        for b in range(100):
            if a_move * a + b_move * b == prize_pos:
                cost = 3 * a + b
                if min_cost is None or cost < min_cost:
                    min_cost = cost

    if min_cost:
        total += min_cost

    # Part 2 - use algebra!
    prize_pos = complex(
        prize_pos.real + 10000000000000, prize_pos.imag + 10000000000000
    )

    # Treat as simultaneous equations
    # a.real + b.real = prize_pos.real
    # a.imag + b.imag = prize_pos.imag
    # multiple by a and prize_pos by opposite b, then subtract result
    a1 = a_move.real * b_move.imag
    p1 = prize_pos.real * b_move.imag

    a2 = a_move.imag * b_move.real
    p2 = prize_pos.imag * b_move.real

    a = (p1 - p2) / (a1 - a2)
    b = (prize_pos.real - a_move.real * a) / b_move.real

    if int(a) == a and int(b) == b:
        total2 += int(3 * a + b)

    i += 4

print(f"Part 1: {total}")
print(f"Part 2: {total2}")
