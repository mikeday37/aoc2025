import sys
from pathlib import Path

def read_input():
    input_path = Path(sys.argv[0]).parent / "input.txt"
    with open(input_path) as file:
        input = file.read()
    return input