from common import *
from math import sqrt
from collections import defaultdict
from time import perf_counter

def parse_input(input):
    return tuple(tuple(int(a) for a in line.split(',')) for line in input.splitlines())

_example = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

def find_closest_pair(points, exclude = set()):
    closest_dist = float(1000 ** 3)
    closest = -1
    for a, (x1, y1, z1) in enumerate(points):
        for b, (x2, y2, z2) in enumerate(points):
            if a != b and not ((a, b) in exclude or (b, a) in exclude):
                dist = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
                if dist < closest_dist:
                    closest_dist = dist
                    closest = (a, b) if a <= b else (b, a)
    return closest

def find_closest_pair_test_helper(points, exclude = set()):
    closest = find_closest_pair(points, exclude)
    return closest, points[closest[0]], points[closest[1]]

test(find_closest_pair_test_helper, ((0, 19), (162,817,812), (425,690,689)), parse_input(_example))
test(find_closest_pair_test_helper, ((0, 7), (162,817,812), (431,825,988)), parse_input(_example), {(0, 19)})
test(find_closest_pair_test_helper, ((2, 13), (906,360,560), (805,96,715)), parse_input(_example), {(0, 19), (0, 7)})

def find_n_closest_pairs(n, points):
    exclude = set()
    for i in range(0, n):
        exclude.add(find_closest_pair(points, exclude))
    return exclude

test(find_n_closest_pairs, {(0, 7), (0, 19), (2, 13)}, 3, parse_input(_example))


start = perf_counter()
brute_force_result = find_n_closest_pairs(1000, parse_input(read_input()))
duration = perf_counter() - start

print(f"Brute Force Solution: {duration:.6f} seconds")
print(brute_force_result)
print(duration)

# note: brute forcing the full input took 210 seconds.