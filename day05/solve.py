from common import *

def parse_input(raw_input):
    lines = raw_input.splitlines()
    blank_at = lines.index("")
    ranges = [(int(a), int(b)) for a, b in (line.split('-') for line in lines[:blank_at])]
    ingredients = [int(a) for a in lines[blank_at + 1:]]
    return (ranges, ingredients)

def count_fresh_ingredients(ranges, ingredients):
    n = 0
    for ingredient in ingredients:
        for range in ranges:
            if ingredient >= range[0] and ingredient <= range[1]:
                n += 1
                break
    return n

def solve_part_1():
    return count_fresh_ingredients(*parse_input(read_input()))

def simplify_ranges(initial_ranges):
    ranges = initial_ranges.copy()
    ranges.sort(key = lambda range: range[0])
    result = []
    last_a, last_b = ranges[0]
    for a, b in ranges[1:]:
        if a > last_b:
            result.append((last_a, last_b))
            last_a, last_b = a, b
        else:
            last_b = max(b, last_b)
    result.append((last_a, last_b))
    return result

def count_in_ranges(ranges):
    return sum(1 + b - a for a, b in simplify_ranges(ranges))

def solve_part_2():
    return count_in_ranges(simplify_ranges(parse_input(read_input())[0]))

print("Part 1:", solve_part_1())
print("Part 2:", solve_part_2())


# ==== Tests ====

_example = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

test(parse_input, ([(3, 5), (10, 14), (16, 20), (12, 18)], [1, 5, 8, 11, 17, 32]), _example)

test(count_fresh_ingredients, 3, *parse_input(_example))

test(simplify_ranges, [(1,3)],          [(1,3), (2,2)])
test(simplify_ranges, [(1,3), (4,5)],   [(1,3), (4,5)])
test(simplify_ranges, [(1,5)],          [(1,3), (2,5)])
test(simplify_ranges, [(3,5), (10,20)], parse_input(_example)[0])

test(count_in_ranges, 3, [(1,2), (3,3)])
test(count_in_ranges, 10, [(1,2), (11,18)])
test(count_in_ranges, 14, simplify_ranges(parse_input(_example)[0]))

verify_known_answer(solve_part_1, 726)
verify_known_answer(solve_part_2, 354226555270043)
