from common import *

def convert_to_roll_set(input: str):
    rolls = set()
    for y, line in enumerate(input.splitlines()):
        for x, value in enumerate(line):
            if value == "@":
                rolls.add((x, y))
    return rolls

def count_neighboring_rolls(x, y, rolls):
    n = 0
    for at_x in range(x - 1, x + 2):
        for at_y in range(y - 1, y + 2):
            if at_x == x and at_y == y:
                continue
            if (at_x, at_y) in rolls:
                n += 1
    return n

def count_accessible_rolls(rolls):
    return sum(count_neighboring_rolls(x, y, rolls) < 4 for x, y in rolls)

def count_removable_rolls(initial_rolls):
    n = 0
    rolls = initial_rolls.copy()
    while True:
        to_remove = [(x, y) for x, y in rolls if count_neighboring_rolls(x, y, rolls) < 4]
        if len(to_remove) == 0:
            break
        for roll in to_remove:
            rolls.remove(roll)
            n += 1
    return n

def solve_part_1():
    rolls = convert_to_roll_set(read_input())
    return count_accessible_rolls(rolls)

def solve_part_2():
    rolls = convert_to_roll_set(read_input())
    return count_removable_rolls(rolls)

print("Part 1:", solve_part_1())
print("Part 2:", solve_part_2())

# --- tests ---

test(convert_to_roll_set, {(1,2)}, """\
..
..
.@""")

test(convert_to_roll_set, {(1,1), (4,1), (3,2)}, """\
......
.@..@.
...@..""")

_example_rolls = convert_to_roll_set("""\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.""")

test(count_neighboring_rolls, 7, 3, 1, _example_rolls)
test(count_neighboring_rolls, 4, 1, 0, _example_rolls)
test(count_neighboring_rolls, 8, 4, 4, _example_rolls)

test(count_accessible_rolls, 13, _example_rolls)

test(count_removable_rolls, 43, _example_rolls)

test(solve_part_1, 1445)
test(solve_part_2, 8317)