from common import *
from .solve import *
from .example import _example

test(parse_input, (
        ((False, True, True, False), ((3,), (1, 3), (2,), (2, 3), (0, 2), (0, 1)), (3, 5, 4, 7)),
        ((False, False, False, True, False), ((0, 2, 3, 4), (2, 3), (0, 4), (0, 1, 2), (1, 2, 3, 4)), (7, 5, 12, 7, 2)),
        ((False, True, True, True, False, True), ((0, 1, 2, 3, 4), (0, 3, 4), (0, 1, 2, 4, 5), (1, 2)), (10, 11, 11, 5, 10, 5)),
    ), _example)

def yield_combinations_test_helper(choices):
    return list(yield_combinations(choices))

test(yield_combinations_test_helper, [[0]], 1)
test(yield_combinations_test_helper, [[0],[1],[0,1]], 2)
test(yield_combinations_test_helper, [[0],[1],[2],[0,1],[0,2],[1,2],[0,1,2]], 3)
test(yield_combinations_test_helper, [
        [0],
        [1],
        [2],
        [3],
        [0, 1],
        [0, 2],
        [0, 3],
        [1, 2],
        [1, 3],
        [2, 3],
        [0, 1, 2],
        [0, 1, 3],
        [0, 2, 3],
        [1, 2, 3],
        [0, 1, 2, 3]
    ], 4)

_parsed_example = parse_input(_example)
_parsed_input = parse_input(read_input())

test(choose_buttons, [1,3], *_parsed_example[0][0:2])
test(solve_part_1, 7, _parsed_example)

def configure_machine_test_helper(parsed_example_row):
    _, buttons, joltages = parsed_example_row
    return sum(configure_machine(buttons, joltages))

test(configure_machine_test_helper, 10, _parsed_example[0])
test(configure_machine_test_helper, 12, _parsed_example[1])
test(configure_machine_test_helper, 11, _parsed_example[2])

verify_known_answer(solve_part_1, 401, _parsed_input)
verify_known_answer(solve_part_2, 15017, _parsed_input)

