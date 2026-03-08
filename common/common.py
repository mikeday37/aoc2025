import sys
from pathlib import Path
import inspect

def read_input():
    input_path = Path(sys.argv[0]).parent / "input.txt"
    with open(input_path) as file:
        input = file.read()
    return input

_test_counter = 0

def test(function, expected_return_value, *args):
    global _test_counter
    _test_counter += 1

    calling_frame = inspect.currentframe().f_back
    calling_filename = calling_frame.f_code.co_filename
    calling_linenumber = calling_frame.f_lineno

    actual_return_value = function(*args)

    if actual_return_value == expected_return_value:
        status = "PASS"
        suffix = ""
    else:
        status = f" !! FAIL !!  (expected={expected_return_value}, actual={actual_return_value})"
        suffix = f" at file \"{calling_filename}\", line {calling_linenumber}"

    print(f"TEST #{_test_counter}, {function.__name__}: {status}{suffix}")
