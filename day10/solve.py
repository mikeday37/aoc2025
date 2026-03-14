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
    total_button_presses = 0
    for lights, buttons, joltages in machines:
        total_button_presses += len(choose_buttons(lights, buttons))
    return total_button_presses

print("Part 1:", solve_part_1(parse_input(read_input())))
        
