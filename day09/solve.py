from common import *
from collections import defaultdict
from typing import NamedTuple, Iterator
from enum import IntEnum
from time import perf_counter
from .util import merge_ranges_inclusive

def parse_input(input):
    return tuple(tuple(int(a) for a in line.split(',')) for line in input.splitlines())

def get_rectangle_sizes_sorted(points, filter = None):
    rects = []
    for i in range(0, len(points) - 1):
        for j in range(i + 1, len(points)):
            (ax, ay), (bx, by) = points[i], points[j]
            if ax > bx:
                ax, bx = bx, ax
            if ay > by:
                ay, by = by, ay
            if filter is not None and not filter((ax, ay), (bx, by)):
                continue
            area = (1 + bx - ax) * (1 + by - ay)
            rects.append((i, j, area))
    rects.sort(key = lambda rect: rect[2])
    return rects

def solve_part_1(points):
    return get_rectangle_sizes_sorted(points)[-1][2]

class Point(NamedTuple):
    x: int
    y: int

class LineType(IntEnum):
    POINT = 0
    VERTICAL = 1
    HORIZONTAL = 2
    DIAGONAL = 3

def categorize_line(p1: Point, p2: Point) -> LineType:
    if p1 == p2:
        return LineType.POINT
    elif p1[0] == p2[0]:
        return LineType.VERTICAL
    elif p1[1] == p2[1]:
        return LineType.HORIZONTAL
    else:
        return LineType.DIAGONAL

def check_orthogonal_intersect(a1: Point, a2: Point, b1: Point, b2: Point) -> bool:
    """
    Return True if the box defined by corners [a1 - a2] intersects with the box defined by
    corners [b1 - b2].  The corners and borders are inclusive.
    """
    return not (
            # horizontally:
            max(a1[0], a2[0]) < min(b1[0], b2[0]) or    # A < B
            min(a1[0], a2[0]) > max(b1[0], b2[0]) or    # A > B
            # vertically:
            max(a1[1], a2[1]) < min(b1[1], b2[1]) or    # A < B
            min(a1[1], a2[1]) > max(b1[1], b2[1])       # A > B
        )

def get_outline(points: tuple[Point]):
    for i in range(0, len(points)):
        yield (points[i], points[i + 1] if i < len(points) - 1 else points[0])

def check_outline_self_intersect(points):
    segments = tuple(get_outline(points))
    for i in range(0, len(segments) - 2):
        for j in range(i + 2, len(segments)):
            if i == 0 and j == len(segments) - 1:
                continue # don't check first against final segment
            if check_orthogonal_intersect(segments[i][0], segments[i][1], segments[j][0], segments[j][1]):
                return True
    return False

class Scanline(NamedTuple):
    "A horizontal scanline from (x1, y) to (x2, y), inclusive.  x1 <= x2 by convention."
    x1: int
    x2: int
    y: int
    
def yield_x_intersections(y: int, verticals: tuple[tuple[Point, Point], ...]) -> Iterator[int]:
    for a, b in verticals:
        if min(a[1], b[1]) <= y < max(a[1], b[1]):
            yield a[0]

def categorize_outline(outline):
    horizontals = defaultdict(list) # key is the y coord, value is (x1, x2) (x-coords of the line endpoints)
    verticals = [] # element is (a, b) (the line endpoints)
    cat = None
    for a, b in outline:
        prev_cat = cat
        cat = categorize_line(a, b)
        assert(cat != prev_cat and cat == LineType.HORIZONTAL or cat == LineType.VERTICAL)
        if cat == LineType.HORIZONTAL:
            horizontals[a[1]].append((a[0], b[0]) if a[0] <= b[0] else (b[0], a[0])) # append (left, right)
        else:
            verticals.append((a, b) if a[1] <= b[1] else (b, a)) # append (top, bottom)
    # sort the verticals list, and the horzontals list for each y coord, on the x coord of first point of each line
    verticals.sort(key = lambda v: v[0][0])
    for y in horizontals.keys():
        horizontals[y].sort(key = lambda h: h[0])
    return horizontals, verticals

def yield_polygon_scanlines(points: tuple[Point, ...]) -> Iterator[Scanline]:
    """
    Return the scanlines that fill the polygon outlined by the given points.
    
    Args:
        points: Tuple of points that define the outline of the polygon.  Must have at least 4 points.
    
    Returns:
        List of scanlines that fill the polygon. Each scanline will individually satisfy x1 <= x2.
    
    Note:
        Each successive pair of input points describes one line in the outline of the polygon.  The
        last point is assumed to link back to the first, so do not repeat the first.  They must
        strictly alternate between horizontal and vertical lines of length greater than zero.  The
        first line can be either horizontal or vertical.

        The returned scanlines will not overlap, but successive scanlines may share the same y
        coordinate if and only if there is a gap between them of at least 1.  Scanlines are sorted first by
        y, then by x1.
    """
    assert(len(points) >= 4)
    assert(points[0] != points[-1])
    outline = tuple(get_outline(points))
    horizontals, verticals = categorize_outline(outline)
    ys = tuple(y for x,y in points)
    y_min, y_max = min(ys), max(ys)
    for y in range(y_min, y_max + 1):
        xs = list(yield_x_intersections(y, verticals))
        xs.sort()
        inside = False
        scanlines_here = []
        i = -1
        start_x = None
        while i < len(xs) - 1:
            i += 1
            inside = not inside
            if inside:
                start_x = xs[i]
            else:
                scanlines_here.append((start_x, xs[i]))
        for a, b in merge_ranges_inclusive(scanlines_here, horizontals[y]):
            yield Scanline(a, b, y)

def is_rect_filled(upper_left, lower_right, scanline_dict) -> bool:
    (ax, ay), (bx, by) = upper_left, lower_right
    assert(ax <= bx and ay <= by)
    for y in range(ay, by + 1):
        if not any([a <= ax and b >= bx for a, b in scanline_dict[y]]):
            return False
    return True
    
def solve_part_2(points):
    scanline_dict = defaultdict(list)
    for x1, x2, y in yield_polygon_scanlines(points):
        scanline_dict[y].append((x1, x2))
    def filter(top_left, bottom_right):
        return is_rect_filled(top_left, bottom_right, scanline_dict)
    return get_rectangle_sizes_sorted(points, filter)[-1][2]

_input_parsed = parse_input(read_input())
print("Part 1:", solve_part_1(_input_parsed))
start = perf_counter()
print("Part 2:", solve_part_2(_input_parsed))
end = perf_counter()
print(f"Part 2 Duration: {end - start:.6f} seconds")


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

test(solve_part_1, 50, parse_input(_example))

test(categorize_line, LineType.POINT, Point(0,0), Point(0,0))
test(categorize_line, LineType.POINT, Point(1,2), Point(1,2))
test(categorize_line, LineType.VERTICAL, Point(1,1), Point(1,2))
test(categorize_line, LineType.HORIZONTAL, Point(1,1), Point(2,1))
test(categorize_line, LineType.DIAGONAL, Point(1,1), Point(2,2))
test(categorize_line, LineType.DIAGONAL, Point(1,2), Point(2,1))
test(categorize_line, LineType.DIAGONAL, Point(2,1), Point(1,2))

test(check_orthogonal_intersect, True,  Point(0,0), Point(0,0),   Point(0,0), Point(0,0))
test(check_orthogonal_intersect, True,  Point(0,0), Point(1,1),   Point(0,0), Point(1,1))
test(check_orthogonal_intersect, True,  Point(1,1), Point(0,0),   Point(0,0), Point(1,1))
test(check_orthogonal_intersect, True,  Point(0,0), Point(3,3),   Point(1,1), Point(2,2))
test(check_orthogonal_intersect, True,  Point(1,1), Point(2,2),   Point(0,0), Point(3,3))
test(check_orthogonal_intersect, True,  Point(0,0), Point(0,1),   Point(0,1), Point(1,1))
test(check_orthogonal_intersect, True,  Point(0,0), Point(10,10), Point(5,5), Point(5,20))
test(check_orthogonal_intersect, False, Point(0,0), Point(1,1),   Point(5,5), Point(6,6))
test(check_orthogonal_intersect, False, Point(0,0), Point(1,1),   Point(5,0), Point(6,1))
test(check_orthogonal_intersect, False, Point(5,0), Point(6,1),   Point(0,0), Point(1,1))
test(check_orthogonal_intersect, False, Point(0,5), Point(1,6),   Point(0,0), Point(1,1))
test(check_orthogonal_intersect, False, Point(0,5), Point(1,6),   Point(0,0), Point(1,1))

test(lambda: tuple(get_outline((
        (0,10),
        (1,11),
        (2,12)
    ))), (
        ((0,10), (1,11)),
        ((1,11), (2,12)),
        ((2,12), (0,10))
    ))

test(check_outline_self_intersect, True, (
#   ....#xxx#
#   ....x...x
#   #xxxxxxx#
#   x...x....
#   #xxx#....
    (5,0),
    (5,5),
    (0,5),
    (0,3),
    (9,3),
    (9,0)
))

test(check_outline_self_intersect, False, (
    (0,0),
    (1,0)
))

test(check_outline_self_intersect, False, (
    (0,0),
    (1,0),
    (1,1),
    (0,1)
))

test(solve_part_1, 50, parse_input(_example))

verify_known_answer(solve_part_1, 4771508457, parse_input(read_input()))

# confirm that the example and full input do not self-intersect (so we can simplify the logic)
test(check_outline_self_intersect, False, _example_parsed)
test(check_outline_self_intersect, False, _input_parsed)

def polyfill_test_helper(points):
    return list(yield_polygon_scanlines(points))

test(polyfill_test_helper, [
        (Scanline(7,11,1)),
        (Scanline(7,11,2)),
        (Scanline(2,11,3)),
        (Scanline(2,11,4)),
        (Scanline(2,11,5)),
        (Scanline(9,11,6)),
        (Scanline(9,11,7)),
    ], _example_parsed)

test(polyfill_test_helper, [
        (Scanline(1,2,1)),
        (Scanline(1,2,2))
    ], [
        (1,1),
        (2,1),
        (2,2),
        (1,2)
    ])

_open_donut_points = [
#   #xxx#.#xxx#
#   x...x.x...x
#   x.#x#.#x#.x
#   x.x.....x.x
#   x.#xxxxx#.x
#   x.........x
#   #xxxxxxxxx#
        (0,0),
        (0,6),
        (10,6),
        (10,0),
        (6,0),
        (6,2),
        (8,2),
        (8,4),
        (2,4),
        (2,2),
        (4,2),
        (4,0)
    ]

_closed_donut_points = [
#   #xxxx##xxx#
#   x....xx...x
#   x.#xx##x#.x
#   x.x.....x.x
#   x.#xxxxx#.x
#   x.........x
#...#xxxxxxxxx#
        (0,0),
        (0,6),
        (10,6),
        (10,0),
        (6,0),
        (6,2),
        (8,2),
        (8,4),
        (2,4),
        (2,2),
        (5,2),
        (5,0)
    ]

test(polyfill_test_helper, [
        (Scanline(0,4,0)),
        (Scanline(6,10,0)),
        (Scanline(0,4,1)),
        (Scanline(6,10,1)),
        (Scanline(0,4,2)),
        (Scanline(6,10,2)),
        (Scanline(0,2,3)),
        (Scanline(8,10,3)),
        (Scanline(0,10,4)),
        (Scanline(0,10,5)),
        (Scanline(0,10,6))
    ], _open_donut_points)

test(polyfill_test_helper, [
        (Scanline(0,10,0)),
        (Scanline(0,10,1)),
        (Scanline(0,10,2)),
        (Scanline(0,2,3)),
        (Scanline(8,10,3)),
        (Scanline(0,10,4)),
        (Scanline(0,10,5)),
        (Scanline(0,10,6))
    ], _closed_donut_points)
