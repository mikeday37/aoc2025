from common import *
from .solve import *
from .example import _example

test(parse_input, {'a': ['b', 'c'], 'd': ['e']}, """\
    d: e
    a: b c
""")

test(parse_input,
    {'aaa': ['you', 'hhh'], 'you': ['bbb', 'ccc'], 'bbb': ['ddd', 'eee'], 'ccc': ['ddd', 'eee', 'fff'], 'ddd': ['ggg'], 'eee': ['out'], 'fff': ['out'], 'ggg': ['out'], 'hhh': ['ccc', 'fff', 'iii'], 'iii': ['out']}
    , _example)

_parsed_example = parse_input(_example)
_parsed_input = parse_input(read_input())

test(solve_part_1, 5, _parsed_example)

verify_known_answer(solve_part_1, 688, _parsed_input)