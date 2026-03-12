from common import *

def parse_input(input):
    lines = [line for line in input.splitlines() if not all(char == '.' for char in line)]
    start = lines[0].index('S')
    splitter_rows = tuple(tuple(index for index, char in enumerate(line) if char == '^') for line in lines[1:])
    return start, splitter_rows

def solve(start, splitter_rows):
    beams = {start}
    beams_per_row = [beams.copy()]
    unique_splitter_hits = 0
    for row in splitter_rows:
        hits = [i for i in row if i in beams]
        unique_splitter_hits += len(hits)
        for i in hits:
            beams.remove(i)
            beams.add(i - 1)
            beams.add(i + 1)
        beams_per_row.append(beams.copy())
    paths = dict.fromkeys(beams_per_row[-1], 1)
    for y in range(len(beams_per_row)-2, -1, -1):
        next_paths = dict()
        for x in beams_per_row[y]:
            if x in beams_per_row[y + 1]:
                next_paths[x] = paths[x]
            else:
                next_paths[x] = paths[x - 1] + paths[x + 1]
        paths = next_paths
    return unique_splitter_hits, paths[start]

splits, timelines = solve(*parse_input(read_input()))
print("Part 1:", splits)
print("Part 2:", timelines)


# ==== Testing Aliases ====

# the solutions were developed and tested separately,
# then combind into one because of considerable code overlap,
# so these testing aliases allowed the tests to be reused after refactoring

def count_splits(input):
    return solve(*parse_input(input))[0]

def count_timelines(input):
    return solve(*parse_input(input))[1]


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

test(parse_input, (7, (
        (7, ),
        (6, 8),
        (5, 7, 9),
        (4, 6, 10),
        (3, 5, 9, 11),
        (2, 6, 12),
        (1, 3, 5, 7, 9, 13)
    )), _example)

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

verify_known_answer(count_splits, 1553, read_input())
verify_known_answer(count_timelines, 15811946526915, read_input())


# ==== Alternate Solution for Part 2 ====

print("-- Alternate Part 2 --")

from functools import cache

@cache
def count_timelines2(y, x, splitter_rows):
    if y >= len(splitter_rows):
        return 1
    if x in splitter_rows[y]:
        return count_timelines2(y + 1, x - 1, splitter_rows) + count_timelines2(y + 1, x + 1, splitter_rows)
    else:
        return count_timelines2(y + 1, x, splitter_rows)
    
test(count_timelines2, 40, 0, *parse_input(_example))
test(count_timelines2, 10, 0, *parse_input(_example2))
verify_known_answer(count_timelines2, 15811946526915, 0, *parse_input(read_input()))
print(count_timelines2.cache_info())


# ==== Comparing the Two Approaches - Runtime ====

import timeit

# read and parse in advance
parsed_input = parse_input(read_input())

# confirm non-recursive still works as expected without wrapper
verify_known_answer(solve, (1553, 15811946526915), *parsed_input)

def count_timelines2_fresh(parsed_input):
    # timing would be trivial and non-representative without clearing the cache before each test
    count_timelines2.cache_clear()
    return count_timelines2(0, *parsed_input)

verify_known_answer(count_timelines2_fresh, 15811946526915, parsed_input)

tries = 100
print(f"-- Part 2 Timing (tries = {tries}) --")
recursive_duration = timeit.timeit(lambda: count_timelines2_fresh(parsed_input), number=tries) / tries
non_recursive_duration = timeit.timeit(lambda: solve(*parsed_input), number=tries) / tries
print(f"Cached Recursive Approach: {recursive_duration:.6f} seconds")
print(f"Non-Recursive Approach: {non_recursive_duration:.6f} seconds")
if recursive_duration > non_recursive_duration:
    print(f"Non-Recursive is faster by a factor of {recursive_duration/non_recursive_duration:.2f} x")
else:
    print(f"Recursive is faster by a factor of {non_recursive_duration/recursive_duration:.2f} x")

# Results on my machine:
#   Across 100 tries, starting with an empty cache each time,
#   the non-recursive approach is consistently over 24 times faster.


# ==== Comparing the Two Approaches - Memory ====

import tracemalloc

def benchmark_memory_usage(function, *args):
    tracemalloc.start()
    result = function(*args)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak / 1024**2 # convert to MB

print("-- Part 2 Memory Usage --")
recursive_usage = benchmark_memory_usage(count_timelines2_fresh, parsed_input)
non_recursive_usage = benchmark_memory_usage(solve, *parsed_input)
print(f"Cached Recursive Approach: {recursive_usage:.3f} MB")
print(f"Non-Recursive Approach: {non_recursive_usage:.3f} MB")
if recursive_usage > non_recursive_usage:
    print(f"Non-Recursive uses {100*(1-non_recursive_usage/recursive_usage):.1f} % less memory")
else:
    print(f"Recursive uses {100*(1-recursive_usage/non_recursive_usage):.1f} % less memory")

# Results on my machine:
#   Starting from an empty cache, the non-recursive approach is 37 % more memory efficient.
#   ...but it's unnecessarily including the unchanging, large splitter_rows tuple in that cache,
#   so that is a potential area for improvement.