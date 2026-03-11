from common import *

def parse_input(input):
    lines = [line for line in input.splitlines() if not all(char == '.' for char in line)]
    start = lines[0].index('S')
    splitter_rows = [[index for index, char in enumerate(line) if char == '^'] for line in lines[1:]]
    return start, splitter_rows

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

def count_timelines(input):
    start, splitter_rows = parse_input(input)
    beams = {start}
    beams_per_row = [beams.copy()]
    for row in splitter_rows:
        hits = [i for i in row if i in beams]
        for i in hits:
            beams.remove(i)
            beams.add(i - 1)
            beams.add(i + 1)
        beams_per_row.append(beams.copy())
    paths_per_position = dict.fromkeys(beams_per_row[-1], 1)
    for y in range(len(beams_per_row)-2, -1, -1):
        next_paths_per_position = dict()
        for x in beams_per_row[y]:
            if x in beams_per_row[y + 1]:
                next_paths_per_position[x] = paths_per_position[x]
            else:
                next_paths_per_position[x] = paths_per_position[x - 1] + paths_per_position[x + 1]
        paths_per_position = next_paths_per_position
    return paths_per_position[start]

print("Part 1:", count_splits(read_input()))
print("Part 2:", count_timelines(read_input()))


# ==== Tests ====

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

test(parse_input, (7, [
        [7],
        [6, 8],
        [5, 7, 9],
        [4, 6, 10],
        [3, 5, 9, 11],
        [2, 6, 12],
        [1, 3, 5, 7, 9, 13]
    ]), _example)

test(count_splits, 21, _example)

test(count_timelines, 4, """\
 S 
 ^ 
^ ^""")
test(count_timelines, 3, """\
 S 
 ^ 
  ^""")
test(count_timelines, 5, """\
 S  
 ^  
  ^ 
^  ^""")
test(count_timelines, 7, """\
 S  
 ^  
^ ^ 
 ^ ^""")

_example2 = """\
    S    
    ^    
     ^   
    ^ ^  
   ^   ^ 
     ^   """
test(count_splits, 7, _example2)
test(count_timelines, 10, _example2)

test(count_timelines, 40, _example)

test(count_splits, 1553, read_input())
test(count_timelines, 15811946526915, read_input())
