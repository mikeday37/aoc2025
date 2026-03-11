from common import *

_example = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

def parse_input(input):
    lines = [line for line in input.splitlines() if not all(char == '.' for char in line)]
    start = lines[0].index('S')
    splitter_rows = [[index for index, char in enumerate(line) if char == '^'] for line in lines[1:]]
    return start, splitter_rows

test(parse_input, (7, [
        [7],
        [6, 8],
        [5, 7, 9],
        [4, 6, 10],
        [3, 5, 9, 11],
        [2, 6, 12],
        [1, 3, 5, 7, 9, 13]
    ]), _example)

def count_splits(input):
    n = 0
    start, splitter_rows = parse_input(input)
    beams = {start}
    for row in splitter_rows:
        hits = [i for i in row if i in beams]
        n += len(hits)
        for i in hits:
            beams.remove(i)
            beams.add(i - 1)
            beams.add(i + 1)
    return n

test(count_splits, 21, _example)

print("Part 1:", count_splits(read_input()))

test(count_splits, 1553, read_input())
