from common import *

def parse_input(input):
    def parse_line(line):
        groups = line.split(' ')
        lights = tuple(ch == '#' for ch in groups[0][1:-1])
        buttons = tuple(tuple(int(x) for x in part[1:-1].split(',')) for part in groups[1:-1])
        joltages = tuple(int(x) for x in groups[-1][1:-1].split(','))
        return lights, buttons, joltages
    return tuple(parse_line(line) for line in input.splitlines())

def yield_combinations(option_count):
    for n in range(1, option_count + 1):
        choices = list(range(0, n))
        increased = True
        while increased:
            yield choices.copy()
            if n == option_count:
                return
            increased = False
            for i in range(n - 1, -1, -1):
                max_here = option_count - n + i
                if choices[i] < max_here:
                    choices[i] += 1
                    increased = True
                    for j in range(i + 1, n):
                        choices[j] = choices[j - 1] + 1
                    break

def choose_buttons(lighting_goal, buttons):
    for choices in yield_combinations(len(buttons)):
        lighting_state = [False] * len(lighting_goal)
        for button_index in choices:
            for light_index in buttons[button_index]:
                lighting_state[light_index] = not lighting_state[light_index]
        if lighting_state == list(lighting_goal):
            return choices
    assert False, "Eric goofed - no combination of single button presses arrives at the goal."

def solve_part_1(machines):
    return sum(len(choose_buttons(lights, buttons)) for lights, buttons, _ in machines)
        
import numpy as np
import scipy.optimize as spo

def get_wiring_matrix(buttons, joltages):
    m = len(joltages)
    n = len(buttons)
    wiring_matrix = np.zeros((m, n), dtype=np.int64)
    for button_index, button in enumerate(buttons):
        for joltage_index in button:
            wiring_matrix[joltage_index, button_index] = 1
    return wiring_matrix

def configure_machine(buttons, joltages):
    n = len(buttons)
    W = get_wiring_matrix(buttons, joltages)
    j = np.array(joltages)
    res = spo.milp(                                # Task: Use Mixed-Integer Linear Programming to find a soltuion with minimal cost
        c=np.ones(n),                              # Cost: Total button presses (equally weighted sum of values in solution vector)
        constraints=spo.LinearConstraint(W, j, j), # Constraint: Exactly solve W * x == j 
        bounds=spo.Bounds(0, max(joltages)),       # Boundary: Each button press count must be between 0 and max joltage inclusive
        integrality=np.ones(n)                     # Integrality: Force the solution to be all integers
    )
    assert res.success, "Eric big goofed - a global standard beast of a number cruncher says there's no solution."
    return res.x.round().astype(int)               # Defensively round answer to nearest integers (internals use floats)

def solve_part_2(machines):
    return sum(sum(configure_machine(buttons, joltages)) for _, buttons, joltages in machines)

_all_machines = parse_input(read_input())
print("Part 1:", solve_part_1(_all_machines))
print("Part 2:", solve_part_2(_all_machines))