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

def solve_for_battery_count(n):
    return sum(pick_best_n_batteries(n, line) for line in read_input().splitlines())

print("Part 1:", solve_for_battery_count(2))
print("Part 2:", solve_for_battery_count(12))


# ==== Tests ====

test(pick_best_n_batteries, 98, 2, "987654321111111")
test(pick_best_n_batteries, 89, 2, "811111111111119")
test(pick_best_n_batteries, 78, 2, "234234234234278")
test(pick_best_n_batteries, 92, 2, "818181911112111")
test(pick_best_n_batteries, 99, 2, "99")

test(pick_best_n_batteries, 811111111119, 12, "811111111111119")
test(pick_best_n_batteries, 987654321111, 12, "987654321111111")
test(pick_best_n_batteries, 434234234278, 12, "234234234234278")
test(pick_best_n_batteries, 888911112111, 12, "818181911112111")
test(pick_best_n_batteries, 999999999999, 12, "999999999999")

test(solve_for_battery_count, 17383, 2)
test(solve_for_battery_count, 172601598658203, 12)