import common

test_input_1 = """\
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

def parse_turn(s):
    a = int(s[1:])
    return a if s[0] == "R" else -a

def count_zeros(turns):
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

if count_zeros(test_input_1) == 3:
    print("TEST 1 PASS")
else:
    print("!! FAIL 1 !!")

if count_all_zeroes(test_input_1) == 6:
    print("TEST 2 PASS")
else:
    print("!! FAIL 2 !!", count_all_zeroes(test_input_1))

test_input_2 = ["R1000"]

if count_all_zeroes(test_input_2) == 10:
    print("TEST 3 PASS")
else:
    print("!! FAIL 3 !!")



input = common.read_input().splitlines()
print("part 1: ", count_zeros(input))
print("part 2: ", count_all_zeroes(input))

print("a ", count_all_zeroes(["R50"]))
print("a ", count_all_zeroes(["R1000"]))
print("a ", count_all_zeroes(["R100"]))
print("a ", count_all_zeroes(["R150"]))
print("a ", count_all_zeroes(["L50"]))
print("a ", count_all_zeroes(["L150"]))
print("a ", count_all_zeroes(["L200"]))
print("a ", count_all_zeroes(["L0"]))
print("a ", count_all_zeroes(["R0"]))
print("------------")
print("a ", count_all_zeroes(["L49","L1"]))
