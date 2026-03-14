from common import *
from itertools import pairwise
from typing import Sequence
import sys


def is_sorted(seq: Sequence[int]) -> bool:
    return all(a <= b for a, b in pairwise(seq))

test(is_sorted, True, [1,2,3])
test(is_sorted, True, [1,1,1])
test(is_sorted, True, [1,2,2])
test(is_sorted, True, [1])
test(is_sorted, True, [])
test(is_sorted, False, [1,0])
test(is_sorted, False, [1,1,0])
test(is_sorted, False, [1,2,1])

    
def merge_consecutive_ranges_inclusive(ranges: Sequence[tuple[int, int]]) -> list[tuple[int, int]]:
    assert all(is_sorted(r) for r in ranges)
    assert is_sorted(a for a, _ in ranges)
    assert all(a[1] < b[0] for a, b in pairwise(ranges))
    if len(ranges) < 2:
        return ranges
    result = []
    cur_start = ranges[0][0]
    i = 0
    while True:
        while i < len(ranges) - 1 and ranges[i][1] + 1 == ranges[i+1][0]:
            i += 1
        result.append((cur_start, ranges[i][1]))
        i += 1
        if i >= len(ranges):
            break
        cur_start = ranges[i][0]
    return result

test(merge_consecutive_ranges_inclusive, [], [])
test(merge_consecutive_ranges_inclusive, [(1,1)], [(1,1)])
test(merge_consecutive_ranges_inclusive, [(1,2)], [(1,2)])
test(merge_consecutive_ranges_inclusive, [(1,2),(4,5)], [(1,2),(4,5)])
test(merge_consecutive_ranges_inclusive, [(1,4)], [(1,2),(3,4)])
test(merge_consecutive_ranges_inclusive, [(1,4),(6,7),(9,36)], [(1,2),(3,4),(6,7),(9,10),(11,22),(23,34),(35,36)])


def merge_ranges_inclusive(ranges1: Sequence[tuple[int, int]], ranges2: Sequence[tuple[int, int]]) -> list[tuple[int, int]]:
    # we expect each range to be pre-sorted in each list
    assert all(is_sorted(r) for r in ranges1)
    assert all(is_sorted(r) for r in ranges2)
    # we also expect the range lists to be sorted on the first value
    assert is_sorted(a for a, _ in ranges1)
    assert is_sorted(a for a, _ in ranges2)
    # we also expect each range list independently to not overlap itself
    assert all(a[1] < b[0] for a, b in pairwise(ranges1))
    assert all(a[1] < b[0] for a, b in pairwise(ranges2))

    i, j = 0, 0 # i and j are indexes into the ranges
    def get_cur_start():
        return min(
            ranges1[i][0] if i < len(ranges1) else sys.maxsize,
            ranges2[j][0] if j < len(ranges2) else sys.maxsize
        )
    cur_start = get_cur_start()
    result = []

    while i < len(ranges1) or j < len(ranges2):
        # check if either currently indexed range is disjointed to the left of any remainder
        # (can occur if they are separated by at least 1 pixel, or we've reached the end of the other sequence)
        disjoint1, disjoint2 = False, False
        if i >= len(ranges1):
            disjoint2 = True
        elif j >= len(ranges2):
            disjoint1 = True
        elif ranges1[i][1] < ranges2[j][0] - 1:
            disjoint1 = True
        elif ranges2[j][1] < ranges1[i][0] - 1:
            disjoint2 = True

        # if neither is disjoint, advance the one with the lesser end (or arbitrarily the first if tied)
        if not disjoint1 and not disjoint2:
            if ranges1[i][1] <= ranges2[j][1]:
                i += 1
            else:
                j += 1
            continue

        # otherwise, create a range from cur_start to the end of the disjointed range, and advance to the next in its sequence
        if disjoint1:
            cur_end = ranges1[i][1]
            i += 1
        elif disjoint2:
            cur_end = ranges2[j][1]
            j += 1
        else:
            assert False # shouldn't get here
        result.append((cur_start, cur_end))
        cur_start = get_cur_start()

    # final pass
    return merge_consecutive_ranges_inclusive(result)

test(merge_ranges_inclusive, [], [], [])
test(merge_ranges_inclusive, [(1,2)], [(1,2)], [])
test(merge_ranges_inclusive, [(1,2)], [], [(1,2)])
test(merge_ranges_inclusive, [(1,4)], [(1,2),(3,4)], [])
test(merge_ranges_inclusive, [(1,4)], [], [(1,2),(3,4)])
test(merge_ranges_inclusive, [(1,2),(4,5)], [], [(1,2),(4,5)])
test(merge_ranges_inclusive, [(1,2),(4,5)], [(1,2),(4,5)], [])

test(merge_ranges_inclusive, [(1,2)], [(1,2)], [(1,2)])
test(merge_ranges_inclusive, [(1,2),(4,5)], [(1,2),(4,5)], [(1,2),(4,5)])

test(merge_ranges_inclusive, [(1,6)], [], [(1,2),(3,4),(5,6)])
test(merge_ranges_inclusive, [(1,6)], [(1,2),(3,4),(5,6)], [])
test(merge_ranges_inclusive, [(1,6)], [(1,2),(5,6)], [(3,4)])
test(merge_ranges_inclusive, [(1,6)], [(3,4)], [(1,2),(5,6)])

test(merge_ranges_inclusive, [(1,4)], [(1,2)], [(3,4)])
test(merge_ranges_inclusive, [(1,4)], [(3,4)], [(1,2)])
test(merge_ranges_inclusive, [(1,4)], [(1,4)], [(2,3)])
test(merge_ranges_inclusive, [(1,4)], [(2,3)], [(1,4)])
    
test(merge_ranges_inclusive, [(1,6),(10,11)], [(1,2),(3,4),(5,6)], [(10,11)])
test(merge_ranges_inclusive, [(1,6),(10,11)], [(10,11)], [(1,2),(3,4),(5,6)])

test(merge_ranges_inclusive, [(1,3)], [(1,2)], [(2,3)])
test(merge_ranges_inclusive, [(1,3)], [(2,3)], [(1,2)])

test(merge_ranges_inclusive, [(1,10),(21,30)], [(1,4),(5,9),(26,30)], [(3,7),(8,10),(21,28)])
test(merge_ranges_inclusive, [(1,10),(21,30)], [(1,4),(6,9),(26,30)], [(3,6),(8,10),(21,28)])
test(merge_ranges_inclusive, [(1,10),(21,30)], [(1,4),(6,9),(26,30)], [(3,7),(8,10),(21,28)])
test(merge_ranges_inclusive, [(1,11),(21,30)], [(1,4),(6,10),(26,30)], [(3,7),(9,11),(21,28)])
test(merge_ranges_inclusive, [(1,10),(21,30)], [(3,7),(8,10),(21,28)], [(1,4),(5,9),(26,30)])
test(merge_ranges_inclusive, [(1,10),(21,30)], [(3,6),(8,10),(21,28)], [(1,4),(6,9),(26,30)])
test(merge_ranges_inclusive, [(1,10),(21,30)], [(3,7),(8,10),(21,28)], [(1,4),(6,9),(26,30)])
test(merge_ranges_inclusive, [(1,11),(21,30)], [(3,7),(9,11),(21,28)], [(1,4),(6,10),(26,30)])
