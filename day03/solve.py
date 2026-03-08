from common import *
    
def pick_best_two_batteries(joltages):
    left = max(joltages[:-1])
    right = max(joltages[joltages.index(left)+1:])
    return int(f"{left}{right}")

def pick_best_twelve_batteries(joltages):
    selection = ""
    skip = 0
    while len(selection) < 12:
        # we're picking one digit, but need room for the remaining digits to be picked after, so:
        keep = 12 - len(selection) - 1
        best = max(joltages[skip:-keep] if keep > 0 else joltages[skip:])
        skip += joltages[skip:].index(best) + 1
        selection = f"{selection}{best}" # really this could just be +=, but I want it clear that this is string concatenation
    return int(selection)

def solve_part(pick_best_batteries):
    return sum(pick_best_batteries(line) for line in read_input().splitlines())

print("Part 1:", solve_part(pick_best_two_batteries))
print("Part 2:", solve_part(pick_best_twelve_batteries))

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

test(lambda: solve_part(pick_best_two_batteries), 17383)
test(lambda: solve_part(pick_best_twelve_batteries), 172601598658203)