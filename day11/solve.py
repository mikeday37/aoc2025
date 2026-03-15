from common import *

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

def count_paths_backward(top_key, string_graph, setup = None, visitor = None):
    graph, ids = get_canonical_graph(string_graph)
    if setup:
        setup(graph, ids)
    back = get_reverse_graph(graph)
    top = ids[top_key]
    n = len(graph)
    remaining = [len(graph[id]) for id in range(0, n)]
    paths = [1 if remaining[id] == 0 else 0 for id in range(0, n)]
    ready = set(id for id in range(0, n) if remaining[id] == 0)
    while ready:
        for id in tuple(ready):
            ready.remove(id)
            paths[id] += sum(paths[child] for child in graph[id])
            if visitor:
                visitor(id, graph, paths)
            for parent in back[id]:
                remaining[parent] -= 1
                assert(remaining[parent] >= 0)
                if remaining[parent] == 0:
                    ready.add(parent)
    return paths[top]

def solve_part_2(string_graph):
    return None

