from operator import attrgetter
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day12_test_input{suffix}.txt"
else:
    input_file = f"day12_input.txt"

data = utils.input_as_lines(input_file)

unassigned = [complex(i, j) for j, line in enumerate(data) for i in range(len(line))]
regions = []


def get_grid(pos):
    x = int(pos.real)
    y = int(pos.imag)
    if x >= 0 and x < len(data[0]) and y >= 0 and y < len(data):
        return data[y][x]


def neighbours_in_region(plot, plant):
    global unassigned
    neighbours = set()
    for step in 1, -1, 1j, -1j:
        neighbour = plot + step
        if neighbour in unassigned and get_grid(neighbour) == plant:
            neighbours.add(neighbour)
            unassigned.remove(neighbour)

    return neighbours


while len(unassigned) > 0:
    plot = unassigned.pop(0)
    plant = get_grid(plot)

    region = set()
    region_univisited = {plot}

    while len(region_univisited) > 0:
        plot = region_univisited.pop()
        next_plots = neighbours_in_region(plot, plant)
        region.add(plot)
        region_univisited = (region_univisited | next_plots) - region

    regions.append((plant, region))

total = 0

for plant, region in regions:
    perimeter = 0
    for plot in region:
        for step in (1, -1, 1j, -1j):
            # if neighbouring plot is not in the region, or if it's at the edge of the grid,
            # this boundary is part of the perimeter
            neighbour = plot + step
            if (
                neighbour.real < 0
                or neighbour.real >= len(data[0])
                or neighbour.imag < 0
                or neighbour.imag >= len(data)
                or neighbour not in region
            ):
                perimeter += 1

    total += len(region) * perimeter

print(f"Part 1: {total}")


# Part 2: get number of straight edges
class Edge:

    def __init__(self, pos, direction, length) -> None:
        self.min_x = pos.real
        self.min_y = pos.imag
        self.direction = direction
        self.length = length

    def is_continuation(self, pos: complex, direction):
        if direction != self.direction:
            return False
        elif pos.real == self.min_x and self.direction == "vertical":
            # Same col, check if row is at either end
            return pos.imag == self.min_y + self.length or pos.imag == self.min_y - 1
        elif pos.imag == self.min_y and self.direction == "horizontal":
            # Same row, check if col is at either end
            return pos.real == self.min_x + self.length or pos.real == self.min_x - 1
        else:
            return False

    def add_pos(self, pos: complex):
        if (
            pos.real == self.min_x
            and self.direction == "vertical"
            and pos.real <= self.min_x + self.length
        ):
            self.min_y = min(self.min_y, pos.imag)
            self.length += 1  # FIXME: check if already within range?
        elif (
            pos.imag == self.min_y
            and self.direction == "horizontal"
            and pos.imag <= self.min_y + self.length
        ):
            self.min_x = min(self.min_x, pos.real)
            self.length += 1
        else:
            raise ValueError

    def __repr__(self) -> str:
        return f"<{self.direction} from ({self.min_x}, {self.min_y}), length {self.length}>"


total = 0

for plant, region in regions:
    perimeter = 0

    # Need to keep track of current edges
    edges = []

    # Sort region by rows then cols, so we (hopefully) don't have to worry about joining edges
    region = sorted(region, key=attrgetter("imag", "real"))

    for plot in region:
        for step in (1, -1, 1j, -1j):
            # if neighbouring plot is not in the region, or if it's at the edge of the grid,
            # this boundary is part of the perimeter
            neighbour = plot + step
            if (
                neighbour.real < 0
                or neighbour.real >= len(data[0])
                or neighbour.imag < 0
                or neighbour.imag >= len(data)
                or neighbour not in region
            ):

                edge_x = neighbour.real if step.real > 0 else plot.real
                edge_y = neighbour.imag if step.imag > 0 else plot.imag
                edge_pos = complex(edge_x, edge_y)
                direction = "vertical" if step in (1, -1) else "horizontal"

                found = False
                for edge in edges:
                    if edge.is_continuation(edge_pos, direction):
                        # Need an extra check here that it's not just a diagonal relationship
                        # e.g. A|B
                        #      -+-
                        #      B|A
                        # Just check in region?
                        if edge_pos == (3 + 3j):
                            breakpoint()
                        print(f"Adding {edge_pos} to {edge}")
                        edge.add_pos(edge_pos)
                        found = True
                        break

                if not found:
                    edges.append(Edge(edge_pos, direction, 1))

    print("******")
    print(plant, len(region), len(edges))
    for edge in edges:
        print(edge)
    print("******")

    total += len(region) * len(edges)

print(f"Part 1: {total}")
# 830893 too low
