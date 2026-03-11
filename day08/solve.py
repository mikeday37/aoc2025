from common import *
from math import sqrt, prod
from collections import defaultdict
from time import perf_counter

def parse_input(input):
    return tuple(tuple(int(a) for a in line.split(',')) for line in input.splitlines())

def find_pair_distances_sorted(points):
    pairs = []
    for a in range(0, len(points) - 1):
        for b in range(a + 1, len(points)):
            (x1, y1, z1), (x2, y2, z2) = points[a], points[b]
            dist = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
            pairs.append((a, b, dist))
    pairs.sort(key = lambda x: x[2])
    return pairs

def find_n_closest_pairs(n, points):
    pairs = find_pair_distances_sorted(points)
    return [(a,b) for (a,b,dist) in pairs][:n]

def collect_circuits(pairs, breaker = None):
    last_circuit_id = 0
    circuits = defaultdict(set)
    point_to_circuit = dict()
    for a, b in pairs:
        if a not in point_to_circuit and b not in point_to_circuit:
            # new circuit
            last_circuit_id += 1
            circuits[last_circuit_id].add(a)
            circuits[last_circuit_id].add(b)
            point_to_circuit[a] = last_circuit_id
            point_to_circuit[b] = last_circuit_id
        elif a in point_to_circuit and b not in point_to_circuit:
            # add b to a's circuit
            id = point_to_circuit[a]
            point_to_circuit[b] = id
            circuits[id].add(b)
        elif b in point_to_circuit and a not in point_to_circuit:
            # add a to b's circuit
            id = point_to_circuit[b]
            point_to_circuit[a] = id
            circuits[id].add(a)
        else:
            # they're both in circuits, so merge unless already the same circuit
            a_id, b_id = point_to_circuit[a], point_to_circuit[b]
            if a_id == b_id:
                continue
            dest_id, source_id = (a_id, b_id) if len(circuits[a_id]) >= len(circuits[b_id]) else (b_id, a_id)
            for p in circuits[source_id]:
                circuits[dest_id].add(p)
                point_to_circuit[p] = dest_id
            del circuits[source_id]
        if breaker is not None and breaker(circuits, point_to_circuit):
            return (a, b)
    # we should have broken before now if there was a breaker
    assert(breaker is None)
    return set(tuple(sorted(point_set)) for point_set in circuits.values()) # easiest structure for test comparison

def solve_part_1(top_n, input):
    circuits = collect_circuits(find_n_closest_pairs(top_n, parse_input(input)))
    sizes = [len(circuit) for circuit in circuits]
    sizes.sort(reverse = True)
    return prod(sizes[:3])

def solve_part_2(input):
    points = parse_input(input)
    pairs = [(a,b) for (a,b,dist) in find_pair_distances_sorted(points)]
    def breaker(circuits, point_to_circuit):
        return len(circuits) == 1 and len(point_to_circuit) == len(points)
    a, b = collect_circuits(pairs, breaker)
    return points[a][0] * points[b][0]

start = perf_counter()
print("Part 1:", solve_part_1(1000, read_input()))
print("Part 2:", solve_part_2(read_input()))
end = perf_counter()
print("Duration:", end - start)


# ==== Tests ====

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

def find_n_closest_pairs_test_helper(n, points):
    return [(points[a], points[b]) for (a, b) in find_n_closest_pairs(n, points)]

test(find_n_closest_pairs_test_helper,
    [
        ((162, 817, 812), (425, 690, 689)),
        ((162, 817, 812), (431, 825, 988)),
        ((906, 360, 560), (805, 96, 715))
    ],
    3, parse_input(_example))

test(collect_circuits, {(1,2,3)}, [(1,2),(2,3)])
test(collect_circuits, {(1,2),(3,4)}, [(1,2),(3,4)])
test(collect_circuits, {(1,2,3),(10,11,12,13)}, [(1,2),(2,3),(10,11),(12,13),(10,12)])
test(collect_circuits, {(1,2,3,10,11,12,13)}, [(1,2),(2,3),(10,11),(12,13),(10,12),(2,12)])
test(collect_circuits, {(1,2,3)}, [(1,2),(3,2)])

test(solve_part_1, 40, 10, _example)
test(solve_part_2, 25272, _example)

verify_known_answer(solve_part_1, 67488, 1000, read_input())
verify_known_answer(solve_part_2, 3767453340, read_input())