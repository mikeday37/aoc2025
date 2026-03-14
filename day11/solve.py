from common import *

def parse_input(input):
    return {
        device[:-1]: outputs
        for device, *outputs in [line.split() for line in input.splitlines()]
    }

def count_paths(start, graph):
    def walk(at):
        if at == "out":
            return 1
        return sum(walk(next) for next in graph[at])
    return walk(start)

def solve_part_1(graph):
    return count_paths("you", graph)
    
print("Part 1:", solve_part_1(parse_input(read_input())))
