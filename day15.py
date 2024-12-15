import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day15_test_input{suffix}.txt"
else:
    input_file = f"day15_input.txt"

data = utils.input_as_lines(input_file)

grid = []
steps = []
bot_pos = None
in_grid = True

step_map = {"<": (-1, 0), "^": (0, -1), ">": (1, 0), "v": (0, 1)}

for j, line in enumerate(data):
    if line == "":
        in_grid = False
        continue

    if in_grid:
        grid.append(list(line))
        x_pos = line.find("@")
        if x_pos >= 0:
            bot_pos = (x_pos, j)
            grid[j][x_pos] = "."
    else:
        steps.extend(list(line))

print(bot_pos)

for step in steps:
    move = step_map[step]
    next_pos = (bot_pos[0] + move[0], bot_pos[1] + move[1])
    if grid[next_pos[1]][next_pos[0]] == ".":
        bot_pos = next_pos
    elif grid[next_pos[1]][next_pos[0]] == "O":
        # breakpoint()
        # Look for the next '.' along the way
        next_empty = next_pos
        while grid[next_empty[1]][next_empty[0]] == "O":
            # Got a box so keep going
            next_empty = (next_empty[0] + move[0], next_empty[1] + move[1])
        if grid[next_empty[1]][next_empty[0]] == ".":
            # Found an empty space so shuffle things along, or actually just swap the first box into the empty space
            grid[next_pos[1]][next_pos[0]] = "."
            grid[next_empty[1]][next_empty[0]] = "O"
            bot_pos = next_pos

    # Otherwise it's a wall and nothing changes


def print_grid(bot_pos):
    print(bot_pos)
    for j, row in enumerate(grid):
        row_str = "".join(row)
        if bot_pos[1] == j:
            row_str = row_str[: bot_pos[0]] + "@" + row_str[bot_pos[0] + 1 :]
        print(row_str)
    print()


# Print the final grid
print_grid(bot_pos)

# Calculate total score
total = 0
for j in range(len(grid)):
    for i in range(len(grid[0])):
        if grid[j][i] == "O":
            total += 100 * j + i

print(f"Part 1: {total}")


# Part 2: rebuild the grid so it's twice as wide
grid = []
bot_pos = None

for j, line in enumerate(data):
    if line == "":
        break

    row = "".join([c * 2 for c in line])
    row = row.replace("OO", "[]")
    grid.append(list(row))
    x_pos = line.find("@")
    if x_pos >= 0:
        bot_pos = (x_pos * 2, j)
        grid[j][x_pos * 2] = "."
        grid[j][x_pos * 2 + 1] = "."

print_grid(bot_pos)


def can_move(pos, move):
    next_pos = (pos[0] + move[0], pos[1] + move[1])
    next_item = grid[next_pos[1]][next_pos[0]]
    if next_item in ("[", "]"):
        # Got a box - see whether the box can move
        if move[1] == 0:
            # Moving left or right, don't need to consider overlapping boxes
            return can_move(next_pos, move)
        else:
            # Need to check whether positions either side can move too
            if next_item == "[":
                other_pos = (next_pos[0] + 1, next_pos[1])
            else:
                other_pos = (next_pos[0] - 1, next_pos[1])
            return can_move(next_pos, move) and can_move(other_pos, move)
    elif next_item == "#":
        return False
    elif next_item == ".":
        return True


def do_move(pos, move, sibling=None):
    "Move item at pos, assuming we've already checked that's OK"
    global grid
    # print("do_move", pos, move)
    next_pos = (pos[0] + move[0], pos[1] + move[1])
    item = grid[pos[1]][pos[0]]
    next_item = grid[next_pos[1]][next_pos[0]]

    if next_item == "#" or item == ".":
        # about to hit a wall, or currenly have an empty space
        return

    if item in ("[", "]"):
        # Got a box - move other boxes too
        if move[1] == 0:
            # Moving left or right, don't need to consider overlapping boxes
            do_move(next_pos, move)
        else:
            # Moving up or down - need to check whether to move boxes either side too
            # Move item beyond this one first
            do_move(next_pos, move)

            # Move item next to this one, if not already moved
            if item == "[":
                other_pos = (pos[0] + 1, pos[1])
            else:
                other_pos = (pos[0] - 1, pos[1])

            if other_pos != sibling:
                do_move(other_pos, move, sibling=pos)  # FIXME

    # Now move current item
    grid[next_pos[1]][next_pos[0]] = item
    grid[pos[1]][pos[0]] = "."


for step in steps:
    move = step_map[step]
    next_pos = (bot_pos[0] + move[0], bot_pos[1] + move[1])
    if grid[next_pos[1]][next_pos[0]] == ".":
        bot_pos = next_pos
    elif grid[next_pos[1]][next_pos[0]] in ("[", "]"):
        if can_move(next_pos, move):
            do_move(next_pos, move, ".")
            bot_pos = next_pos

    # print(f"Moved {step}")
    # print_grid(bot_pos)
    # breakpoint()

print_grid(bot_pos)
# Calculate total score
total = 0
for j in range(len(grid)):
    for i in range(len(grid[0])):
        if grid[j][i] == "[":
            total += 100 * j + i

print(f"Part 2: {total}")
# Answer too low!
