from common import *
    
def pick_best_batteries(joltages):
    left_digit = max(joltages[:-1])
    right_digit = max(joltages[joltages.index(left_digit)+1:])
    return int(left_digit + right_digit)

test(pick_best_batteries, 98, "987654321111111")
test(pick_best_batteries, 89, "811111111111119")
test(pick_best_batteries, 78, "234234234234278")
test(pick_best_batteries, 92, "818181911112111")
test(pick_best_batteries, 99, "99")

