import common

test_1_input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

def is_invalid_id(id):
    s = str(id)
 
    # invalid ids have even length
    if len(s) % 2 != 0:
        return False
    
    # invalid ids have the first half matching the last
    half = int(len(s)/2)
    return s[:half] == s[half:]

def get_invalid_id_sum(range_from, range_to):
    invalid_sum = 0
    for id in range(range_from, range_to+1):
        if is_invalid_id(id):
            invalid_sum += id
    return invalid_sum

def solve_part_1(input):
    invalid_sum = 0
    for range in input.split(','):
        range_from, range_to = [int(x) for x in range.split('-')]
        invalid_sum += get_invalid_id_sum(range_from, range_to)
    return invalid_sum

test_1_result = solve_part_1(test_1_input)
print("Test 1: ", "Pass" if test_1_result == 1227775554 else f"!! FAIL !! ({test_1_result})")

part_1_result =  solve_part_1(common.read_input())
print("Part 1:", part_1_result, "|", "Pass" if part_1_result == 17077011375 else f"!! FAIL !! ({part_1_result})")
                        