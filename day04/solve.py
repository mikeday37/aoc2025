from common import *

_example_input = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

def count_neighbors(x: int, y: int, diagram: list[str], width: int, height: int) -> int:
    n = 0
    # interval to check will be [start, end)
    start_x = x - 1 if x > 0 else 0
    start_y = y - 1 if y > 0 else 0
    end_x = x + 2 if x < width - 1 else width
    end_y = y + 2 if y < height - 1 else height
    for at_y in range(start_y, end_y):
        for at_x in range(start_x, end_x):
            if (at_y == y and at_x == x):
                continue
            if diagram[at_y][at_x] == "@":
                n += 1
    return n

test(count_neighbors, 8, 1, 1, ["@@@","@@@","@@@"], 3, 3)
test(count_neighbors, 7, 1, 1, ["@@@","@@.","@@@"], 3, 3)
test(count_neighbors, 1, 1, 1, ["...","..@","..."], 3, 3)
test(count_neighbors, 3, 1, 0, ["@@","@@"], 2, 2)
test(count_neighbors, 3, 0, 1, ["@@","@@"], 2, 2)
test(count_neighbors, 0, 0, 0, ["@"], 1, 1)

def count_accessible_rolls(diagram_raw: str) -> int:
    n = 0
    diagram = diagram_raw.splitlines()
    width = len(diagram[0])
    height = len(diagram)
    for y in range(0, height):
        for x in range(0, width):
            if diagram[y][x] != "@":
                continue
            neighbors = count_neighbors(x, y, diagram, width, height)
            if neighbors < 4:
                n += 1
    return n

test(count_accessible_rolls, 13, _example_input)

def solve_part_1():
    return count_accessible_rolls(read_input())

test(solve_part_1, 1445)

print("Part 1:", solve_part_1())


