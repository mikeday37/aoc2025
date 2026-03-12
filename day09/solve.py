from common import *

def parse_input(input):
    return tuple(tuple(int(a) for a in line.split(',')) for line in input.splitlines())

def get_rectangle_sizes_sorted(points):
    rects = []
    for i in range(0, len(points) - 1):
        for j in range(i + 1, len(points)):
            (ax, ay), (bx, by) = points[i], points[j]
            if ax > bx:
                ax, bx = bx, ax
            if ay > by:
                ay, by = by, ay
            area = (1 + bx - ax) * (1 + by - ay)
            rects.append((i, j, area))
    rects.sort(key = lambda rect: rect[2])
    return rects

def solve_part_1(points):
    return get_rectangle_sizes_sorted(points)[-1][2]

_input_parsed = parse_input(read_input())
print("Part 1:", solve_part_1(_input_parsed))


# ==== Tests ==== 

_example = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

_example_parsed = parse_input(_example)
test(solve_part_1, 50, _example_parsed)
verify_known_answer(solve_part_1, 4771508457, _input_parsed)