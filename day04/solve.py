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

def convert_to_roll_set(input: str):
    rolls = set()
    for y, line in enumerate(input.splitlines()):
        for x, value in enumerate(line):
            if value == "@":
                rolls.add((x, y))
    return rolls

test(convert_to_roll_set, {(1,2)}, """\
..
..
.@""")

test(convert_to_roll_set, {(1,1), (4,1), (3,2)}, """\
......
.@..@.
...@..""")

def count_neighboring_rolls(x, y, rolls):
    n = 0
    for at_x in range(x - 1, x + 2):
        for at_y in range(y - 1, y + 2):
            if at_x == x and at_y == y:
                continue
            if (at_x, at_y) in rolls:
                n += 1
    return n

_example_rolls = convert_to_roll_set(_example_input)
test(count_neighboring_rolls, 7, 3, 1, _example_rolls)
test(count_neighboring_rolls, 4, 1, 0, _example_rolls)
test(count_neighboring_rolls, 8, 4, 4, _example_rolls)

def count_accessible_rolls(rolls):
    return sum(1 for x, y in rolls if count_neighboring_rolls(x, y, rolls) < 4)

test(count_accessible_rolls, 13, _example_rolls)

def solve_part_1():
    rolls = convert_to_roll_set(read_input())
    return count_accessible_rolls(rolls)

test(solve_part_1, 1445)

print("Part 1:", solve_part_1())

