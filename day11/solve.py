from common import *
from timeit import timeit

def parse_input(input):
    return {
        device[:-1]: outputs
        for device, *outputs in [line.split() for line in input.splitlines()]
    }

def count_paths(start, string_graph):
    def walk(at):
        if at == "out":
            return 1
        return sum(walk(next) for next in string_graph[at])
    return walk(start)

def solve_part_1(string_graph):
    return count_paths("you", string_graph)


def get_canonical_graph(string_graph):
    ids = {key: index for index, key in enumerate(string_graph)}
    return [[ids[next] for next in string_graph[key] if next != "out"] for key in string_graph], ids

def get_reverse_graph(graph):
    n = len(graph)
    reverse = [[] for _ in range(0, n)]
    for id in range(0, n):
        for next in graph[id]:
            reverse[next].append(id)
    return reverse

def visit_graph_backward(graph, reverse, setup = None, visitor = None):
    assert list(map(sorted, reverse)) == list(map(sorted, get_reverse_graph(graph))), "reverse must be the reverse of graph"
    n = len(graph)
    remaining = [len(graph[id]) for id in range(0, n)]
    ready = set(id for id in range(0, n) if remaining[id] == 0)
    assert ready, "graph must have bottom nodes"
    if setup:
        setup(remaining)
    while ready:
        for id in tuple(ready):
            ready.remove(id)
            if visitor:
                visitor(id)
            for parent in reverse[id]:
                remaining[parent] -= 1
                assert(remaining[parent] >= 0)
                if remaining[parent] == 0:
                    ready.add(parent)
    assert all(remaining[id] == 0 for id in range(0, n)), "all nodes must be visited"

def count_fft_dac_paths(top_key, string_graph):
    graph, ids = get_canonical_graph(string_graph)
    reverse = get_reverse_graph(graph)    
    n = len(graph)
    below_fft, below_dac = [False] * n, [False] * n
    above_fft, above_dac = [False] * n, [False] * n
    paths = []

    # 1st pass - mark all nodes above (or at) fft/dac
    def mark_above(id):
        if id == ids["fft"]:
            above_fft[id] = True
        else:
            above_fft[id] = any(above_fft[child] for child in graph[id])
        if id == ids["dac"]:
            above_dac[id] = True
        else:
            above_dac[id] = any(above_dac[child] for child in graph[id])
    visit_graph_backward(graph, reverse, None, mark_above)

    # 2nd pass - mark all nodes below (or at) fft/dac
    def mark_below(id):
        if id == ids["fft"]:
            below_fft[id] = True
        else:
            below_fft[id] = any(below_fft[parent] for parent in reverse[id])
        if id == ids["dac"]:
            below_dac[id] = True
        else:
            below_dac[id] = any(below_dac[parent] for parent in reverse[id])
    visit_graph_backward(reverse, graph, None, mark_below)

    # final pass - count paths that include both
    def is_on_path(id):
        return (above_fft[id] or below_fft[id]) and (above_dac[id] or below_dac[id])
    def setup(remaining):
        nonlocal paths
        paths = [1 if remaining[id] == 0 and is_on_path(id) else 0 for id in range(0, n)]
    def count(id):
        paths[id] += sum(paths[child] for child in graph[id] if is_on_path(id))
    visit_graph_backward(graph, reverse, setup, count)

    return paths[ids[top_key]]

def solve_part_2(string_graph):
    return count_fft_dac_paths("svr", string_graph)


_parsed_input = parse_input(read_input())
print("Part 1:", solve_part_1(_parsed_input))
print("Part 2:", solve_part_2(_parsed_input))


print()
tries = 100
part2_duration = timeit(lambda: solve_part_2(_parsed_input), number=tries) / tries
print(f"Part 2 duration: {part2_duration:.6f} seconds")
print(f"Part 2 answer with commas: {solve_part_2(_parsed_input):,}") # for reading convenience
