import sys
from dataclasses import dataclass, field
from typing import Optional

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day18_test_input{suffix}.txt"
else:
    input_file = f"day18_input.txt"

data = utils.input_as_lines(input_file)

space_size = 7 if test_mode else 71
n_bytes = 12 if test_mode else 1024
start_pos = complex(0, 0)
end_pos = complex(space_size - 1, space_size - 1)
byte_map = set()

for line in data[:n_bytes]:
    coords = [int(n) for n in line.split(",")]
    byte_map.add(complex(coords[0], coords[1]))

# Add boundaries to the map
for i in range(-1, space_size + 1):
    byte_map.add(complex(i, -1))
    byte_map.add(complex(i, space_size))

for j in range(-1, space_size + 1):
    byte_map.add(complex(-1, j))
    byte_map.add(complex(space_size, j))


def print_map(byte_map):
    for j in range(-1, space_size + 1):
        for i in range(-1, space_size + 1):
            if complex(i, j) in byte_map:
                print("#", end="")
            else:
                print(".", end="")
        print()


print_map(byte_map)


# Class used in A* to represent a node and its f, g, h values
@dataclass
class Cell:
    pos: complex
    parent: Optional["Cell"]
    f: float = field(init=False)  # Total of g + h, used to
    g: float = field(init=False)  # Distance from start
    h: float = field(init=False)  # Heuristic (low bound) distance to end

    def __post_init__(self):
        self.f = 0
        self.g = 0
        self.h = abs(end_pos - self.pos)

    def __eq__(self, other):
        return self.pos == other.pos

    def __repr__(self):
        return f"Cell(pos={self.pos}, parent={self.parent.pos if self.parent else None}, f={self.f:.3f}, g={self.g:.3f}, h={self.h:.3f})"


# A* algorithm implementation, inspired by tutorial at https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
def a_star():
    open_list = [Cell(start_pos, parent=None)]
    closed_list = []

    while open_list:
        open_list.sort(key=lambda c: c.f)
        current = open_list.pop(0)
        closed_list.append(current.pos)

        if current.pos == end_pos:
            # found the end - follow back to get the path
            path = []
            current_in_path = current
            while current_in_path is not None:
                path.append(current_in_path.pos)
                current_in_path = current_in_path.parent

            return path[::-1]  # Return reversed path
        else:
            children = [Cell(current.pos + step, current) for step in (1, -1, 1j, -1j)]

            for child in children:
                if child.pos in closed_list or child.pos in byte_map:
                    continue

                child.g = current.g + 1
                child.f = child.g + child.h

                existing_cell = next((c for c in open_list if c.pos == child.pos), None)
                if existing_cell and child.g >= existing_cell.g:
                    continue
                else:
                    open_list.append(child)


print(f"Finding path from {start_pos} to {end_pos}")
path = a_star()
n_steps = len(path) - 1  # Path includes start pos so subtract 1 for number of steps
print(f"Part 1: {n_steps}")

# Part 2: find the point at which our path is blocked

while True:
    line = data[n_bytes]
    coords = [int(n) for n in line.split(",")]
    byte_map.add(complex(coords[0], coords[1]))

    path = a_star()

    if path is None:
        break

    n_bytes += 1

print(f"Part 2: {data[n_bytes]}")
