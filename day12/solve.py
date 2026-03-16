from common import *
from timeit import timeit

def mirror(form):
    return tuple(tuple(reversed(row)) for row in form)

def rotate_right(form):
    w, h = len(form[0]), len(form)
    result = [[None] * h for _ in range(0, w)]
    for sx in range(0, w):
        for sy in range(0, h):
            x, y = h - 1 - sy, sx
            result[y][x] = form[sy][sx]
    return tuple(tuple(row) for row in result)

class Shape:
    definition: tuple[str]
    def_width: int
    def_height: int
    forms: tuple[tuple[tuple[bool, ...], ...]]
    area: int

    def __init__(self, lines):
        self.definition = tuple(lines)
        self.def_width = len(self.definition[0])
        self.def_height = len(self.definition)
        first_form = tuple(tuple(ch == '#' for ch in line) for line in lines)
        forms = [first_form, mirror(first_form)]
        cur_form = first_form
        for n in range(0, 3):
            cur_form = rotate_right(cur_form)
            forms.append(cur_form)
            forms.append(mirror(cur_form))
        self.forms = tuple(set(forms))
        self.area = sum(sum(row) for row in forms[0])

class Region:
    width: int
    height: int
    presents: list[int]

    def __init__(self, line):
        dims, *presents = line.split()
        self.width, self.height = map(int, dims[:-1].split('x'))
        self.presents = tuple(map(int, presents))

def parse_input(input):
    shapes = []
    regions = []
    lines = input.splitlines()
    start = 0
    for i, line in enumerate(lines):
        if not line:
            shapes.append(Shape(lines[start+1:i])) # safely ignore the index heading
            start = i + 1
    for i in range(start, len(lines)):
        regions.append(Region(lines[i]))
    return tuple(shapes), tuple(regions)
    
# NOTE: This puzzle was unexpectedly solved during analysis of the data.  See: analysis.py