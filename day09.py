import copy
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day09_test_input{suffix}.txt"
else:
    input_file = f"day09_input.txt"

data = utils.input_as_string(input_file)

blocks = []

for i, n in enumerate(data):
    if i % 2 == 0:
        # even index is file
        blocks.extend([i // 2] * int(n))

    else:
        # odd index is free space
        blocks.extend([None] * int(n))

blocks2 = copy.deepcopy(blocks)

i = 0
while i < len(blocks) - 1:
    if blocks[i] is None:
        blocks[i] = blocks.pop()
    else:
        i += 1

while blocks[-1] is None:
    blocks.pop()

checksum = 0

for i, n in enumerate(blocks):
    checksum += i * n

print(f"Part 1: {checksum}")

i = len(data) - 1
last_idx = len(blocks2) - 1

# Part 2: iterate over original data again to find blocks and ranges
data = [int(c) for c in data]
files_map = {}
spaces_map = []

j = 0
for i, n in enumerate(data):
    if i % 2 == 0:
        files_map[i // 2] = (j, j + n)
    else:
        spaces_map.append((j, j + n))

    j += n


indices = reversed(files_map.keys())

for i in indices:
    block_len = data[i * 2]
    for j, s in enumerate(spaces_map):
        # If the space is further right than the file, we can't carry on
        if s[0] > files_map[i][0]:
            break

        if s[1] - s[0] >= block_len:
            prev_idx = j // 2
            files_map[i] = (s[0], s[0] + block_len)
            if block_len == s[1] - s[0]:
                # Filled the space so remove it
                spaces_map.pop(j)
            else:
                spaces_map[j] = (s[0] + block_len, s[1])

            break


checksum = 0

for n, (i, j) in files_map.items():
    for k in range(i, j):
        checksum += n * k

print(f"Part 2: {checksum}")
# Answer too high!
