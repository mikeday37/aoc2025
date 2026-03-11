from common import *

def parse_turn(s):
    a = int(s[1:])
    return a if s[0] == "R" else -a

def count_zeroes(turns):
    zeroes = 0
    v = 50
    for turn in turns:
        amount = parse_turn(turn)
        v = (v + amount) % 100
        if v == 0:
            zeroes += 1
    return zeroes

def count_all_zeroes(turns):
    zeroes = 0
    v = 50
    for turn in turns:
        amount = parse_turn(turn)
        if amount > 0:
            zeroes += int((v + amount)/100)
        else:
            zeroes += int(((-v)%100 - amount)/100)
        v = (v + amount) % 100
    return zeroes

_input = read_input().splitlines()
print("part 1: ", count_zeroes(_input))
print("part 2: ", count_all_zeroes(_input))


# ==== Tests ====

_example = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
""".splitlines()

test(count_zeroes, 3, _example)
test(count_all_zeroes, 6, _example)
test(count_all_zeroes, 10, ["R1000"])

test(count_all_zeroes, 1, (["R50"]))
test(count_all_zeroes, 10, (["R1000"]))
test(count_all_zeroes, 1, (["R100"]))
test(count_all_zeroes, 2, (["R150"]))
test(count_all_zeroes, 1, (["L50"]))
test(count_all_zeroes, 2, (["L150"]))
test(count_all_zeroes, 2, (["L200"]))
test(count_all_zeroes, 0, (["L0"]))
test(count_all_zeroes, 0, (["R0"]))
test(count_all_zeroes, 1, (["L49","L1"]))

verify_known_answer(count_zeroes, 1007, _input)
verify_known_answer(count_all_zeroes, 5820, _input)
