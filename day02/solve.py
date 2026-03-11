from common import *

def is_invalid_part_1(id):
    s = str(id)
    if len(s) % 2 != 0:
        return False
    half = int(len(s)/2)
    return s[:half] == s[half:]

def is_invalid_part_2(id):
    s = str(id)
    for prefix_len in range(1, int(len(s)/2)+1):
        prefix = s[:prefix_len]
        if len(s) % prefix_len != 0:
            continue
        repeat_count = int(len(s) / prefix_len)
        if s == prefix * repeat_count:
            return True
    return False

def solve_part(input, is_invalid):
    invalid_sum = 0
    for raw_range in input.split(','):
        range_from, range_to = [int(x) for x in raw_range.split('-')]
        for id in range(range_from, range_to+1):
            if is_invalid(id):
                invalid_sum += id
    return invalid_sum

_input = read_input()
print("Part 1:", solve_part(_input, is_invalid_part_1))
print("Part 2:", solve_part(_input, is_invalid_part_2))


# ==== Tests ====

_example = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

test(solve_part, 1227775554, _example, is_invalid_part_1)
test(solve_part, 4174379265, _example, is_invalid_part_2)

verify_known_answer(solve_part, 17077011375, _input, is_invalid_part_1)
verify_known_answer(solve_part, 36037497037, _input, is_invalid_part_2)
