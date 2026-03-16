from common import *
from .solve import *
from .example import _example

test(mirror, ((False, True),), ((True, False),))
test(mirror, ((0,1,2),), ((2,1,0),))
test(mirror, (
        (0,1),
        (2,3),
        (4,5)
    ), (
        (1,0),
        (3,2),
        (5,4)
    ))

test(rotate_right, (
        (0,1),
        (2,3),
        (4,5)
    ), (
        (1,3,5),
        (0,2,4)
    ))

def check_shape_area_and_form_count(lines):
    s = Shape(lines)
    return s.area, len(s.forms)

test(check_shape_area_and_form_count, (4, 8), ["##.", ".#.", ".#."])
test(check_shape_area_and_form_count, (7, 2), ["###", ".#.", "###"])
test(check_shape_area_and_form_count, (5, 4), ["##.", ".#.", ".##"])
test(check_shape_area_and_form_count, (7, 4), ["###", "..#", "###"])
