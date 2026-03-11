from common import *
from math import prod

def is_column_blank(column_index, input):
    return all(line[column_index] == ' ' for line in input)

def chop_columns(raw_input):
    input = raw_input.splitlines()
    width, height = len(input[0]), len(input)
    blocks = []
    block_start = 0
    for column_index in range(1, width):
        if is_column_blank(column_index, input):
            blocks.append([line[block_start:column_index] for line in input])
            block_start = column_index + 1
    blocks.append([line[block_start:] for line in input])
    return blocks

def transpose_block(input):
    return [''.join(row) for row in zip(*input)]

def solve_block(block, transpose = False):
    inputs = [int(x.strip()) for x in (transpose_block(block[:-1]) if transpose else block[:-1])]
    match block[-1].strip():
        case '+':
            return sum(inputs)
        case '*':
            return prod(inputs)

def solve_part(input, transpose = False):
    return sum(solve_block(block, transpose) for block in chop_columns(input))

print("Part 1:", solve_part(read_input()))
print("Part 2:", solve_part(read_input(), True))


# ==== Tests ====

test(chop_columns, [['a', 'x', 'p'], ['bb', 'y ', ' d'], [' c', 'zq', 'q ']], """\
a bb  c
x y  zq
p  d q """)

test(transpose_block, ["abc","xyz"], ["ax", "by", "cz"])

test(solve_block, 3, [' 1','2 ',' +'])
test(solve_block, 0, ['9','0','*'])

_example = """\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

test(solve_part, 4277556, _example)
test(solve_part, 3263827, _example, True)

verify_known_answer(solve_part, 4722948564882, read_input())
verify_known_answer(solve_part, 9581313737063, read_input(), True)