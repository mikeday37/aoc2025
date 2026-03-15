from common import *
from .solve import *
from .example import _example, _example2

test(parse_input, {'a': ['b', 'c'], 'd': ['e']}, """\
    d: e
    a: b c
""")

test(parse_input,
    {'aaa': ['you', 'hhh'], 'you': ['bbb', 'ccc'], 'bbb': ['ddd', 'eee'], 'ccc': ['ddd', 'eee', 'fff'], 'ddd': ['ggg'], 'eee': ['out'], 'fff': ['out'], 'ggg': ['out'], 'hhh': ['ccc', 'fff', 'iii'], 'iii': ['out']}
    , _example)

_parsed_test = parse_input("a: b\nb: c d\nc: out\nd: c")

test(get_canonical_graph, (
        [[1], [2,3], [], [2]], 
        {"a": 0, "b": 1, "c": 2, "d": 3}
    ), _parsed_test)

test(get_reverse_graph, [[], [0], [1,3], [1]], get_canonical_graph(_parsed_test)[0])

_test_def = """\
    a: b c h i
    b: d
    c: d e
    d: f g
    e: out
    f: g
    g: out
    h: c
    i: h
"""

_parsed_example, _parsed_example2, _parsed_input, _parsed_test = [parse_input(e) for e in [_example, _example2, read_input(), _test_def]]

test(count_paths, 11, "a", _parsed_test)
test(count_paths, 5, "you", _parsed_example)
test(count_paths, 8, "svr", _parsed_example2)

test(count_paths_backward, 11, "a", _parsed_test)
test(count_paths_backward, 5, "you", _parsed_example)
test(count_paths_backward, 8, "svr", _parsed_example2)

test(solve_part_1, 5, _parsed_example)

verify_known_answer(solve_part_1, 688, _parsed_input)
verify_known_answer(count_paths_backward, 688, "you", _parsed_input)