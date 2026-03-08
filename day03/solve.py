from common import *

def pick_best_n_batteries(n, joltages):
    selection = ""
    skip = 0
    while len(selection) < n:
        keep = n - len(selection) - 1
        best = max(joltages[skip:-keep] if keep > 0 else joltages[skip:])
        skip += joltages[skip:].index(best) + 1
        selection += best
    return int(selection)

def solve_part(pick_best_batteries):
    return sum(pick_best_batteries(line) for line in read_input().splitlines())

print("Part 1:", solve_part(lambda x: pick_best_n_batteries(2, x)))
print("Part 2:", solve_part(lambda x: pick_best_n_batteries(12, x)))

def pick_best_two_batteries(joltages):
    return pick_best_n_batteries(2, joltages)

def pick_best_twelve_batteries(joltages):
    return pick_best_n_batteries(12, joltages)

test(pick_best_two_batteries, 98, "987654321111111")
test(pick_best_two_batteries, 89, "811111111111119")
test(pick_best_two_batteries, 78, "234234234234278")
test(pick_best_two_batteries, 92, "818181911112111")
test(pick_best_two_batteries, 99, "99")

test(pick_best_twelve_batteries, 811111111119, "811111111111119")
test(pick_best_twelve_batteries, 987654321111, "987654321111111")
test(pick_best_twelve_batteries, 434234234278, "234234234234278")
test(pick_best_twelve_batteries, 888911112111, "818181911112111")
test(pick_best_twelve_batteries, 999999999999, "999999999999")

test(lambda: solve_part(lambda x: pick_best_n_batteries(2, x)), 17383)
test(lambda: solve_part(lambda x: pick_best_n_batteries(12, x)), 172601598658203)