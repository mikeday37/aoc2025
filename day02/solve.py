import common

test_1_input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

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

test_1_result = solve_part(test_1_input, is_invalid_part_1)
print("Test 1: ", "Pass" if test_1_result == 1227775554 else f"!! FAIL !! ({test_1_result})")

test_2_result = solve_part(test_1_input, is_invalid_part_2)
print("Test 2: ", "Pass" if test_2_result == 4174379265 else f"!! FAIL !! ({test_2_result})")

part_1_result =  solve_part(common.read_input(), is_invalid_part_1)
print("Part 1:", part_1_result, "|", "Pass" if part_1_result == 17077011375 else f"!! FAIL !! ({part_1_result})")

part_2_result =  solve_part(common.read_input(), is_invalid_part_2)
print("Part 2:", part_2_result, "|", "Pass" if part_2_result == 36037497037 else f"!! FAIL !! ({part_2_result})")
