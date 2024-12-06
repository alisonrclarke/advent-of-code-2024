from collections import defaultdict
import math
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ''
    input_file = f'day05_test_input{suffix}.txt'
else:
    input_file = f'day05_input.txt'

data = utils.input_as_lines(input_file)

pages_before = defaultdict(set)
pages_after = defaultdict(set)

i = 0

# Process page ordering rules
while i < len(data):
    line = data[i]
    if line == '':
        break

    x, y = line.split('|')
    pages_after[x].add(y)
    pages_before[y].add(x)

    i += 1

# Now process updates
total = 0
total2 = 0

i+=1
while i < len(data):
    line = data[i]
    pages = line.split(',')
    valid = True
    for j, p in enumerate(pages):
        if any(p2 in pages_after[p] for p2 in pages[:j]) or any(p2 in pages_before[p] for p2 in pages[j+1:]):
            valid = False
            break

    if valid:
        total += int(pages[len(pages)//2])
    else:
        # Part 2: try to get the list in order
        ordered = pages[:1]
        j = 1
        # Then go through the rest and work out where they should go
        while j < len(pages):
            p = pages[j]
            for k, p2 in enumerate(ordered):
                if p in pages_before[p2]:
                    ordered.insert(k, p)
                    break

            if p not in ordered:
                ordered.append(p)

            # print(ordered)

            j += 1

        total2 += int(ordered[len(ordered)//2])
            
    
    i += 1

print(f"Part 1: {total}")
print(f"Part 2: {total2}")