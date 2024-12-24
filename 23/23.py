#!/usr/bin/env python3

# https://adventofcode.com/2024/day/23 - "LAN Party"
# Author: Greg Hamerly

import sys

def cliques(partial, state, u, original_degree, remaining_degree, graph, seen):
    if remaining_degree == 0:
        yield tuple(sorted(partial))
        return

    if len(graph[u]) < original_degree:
        return

    if not partial <= graph[u]:
        return

    state |= (1 << u)

    # key speedup
    if state in seen:
        return

    seen.add(state)

    partial.add(u)

    possibilities = set()
    for v in partial:
        possibilities.update(graph[v])
    possibilities -= partial

    if len(possibilities) >= remaining_degree:
        for v in possibilities:
            yield from cliques(partial, state, v, original_degree, remaining_degree - 1, graph, seen)

    partial.remove(u)

def construct_graph(data):
    vertices = {u for u, v in data} | {v for u, v in data}
    vertex_id = {u: uid for uid, u in enumerate(sorted(vertices))}
    vertex_lookup = sorted(vertices)
    graph = {u: set() for u in vertex_id.values()}

    for u, v in data:
        graph[vertex_id[u]].add(vertex_id[v])
        graph[vertex_id[v]].add(vertex_id[u])

    return vertex_lookup, vertex_id, graph

def part1(data):
    vertex_lookup, vertex_id, graph = construct_graph(data)

    triangles = set()
    seen = set()
    for u in vertex_id.values():
        for c in cliques(set(), 0, u, 3, 3, graph, seen):
            if any(vertex_lookup[x].startswith('t') for x in c):
                triangles.add(tuple(sorted(c)))

    return len(triangles)

def part2(data):
    vertices = {u for u, v in data} | {v for u, v in data}
    vertex_id = {u: uid for uid, u in enumerate(sorted(vertices))}
    vertex_lookup = sorted(vertices)
    graph = {u: set() for u in vertex_id.values()}

    for u, v in data:
        graph[vertex_id[u]].add(vertex_id[v])
        graph[vertex_id[v]].add(vertex_id[u])

    max_degree = max(map(len, graph.values()))

    for degree in range(max_degree, 2, -1):
        seen = set()
        for u in vertex_id.values():
            if len(graph[u]) >= degree:
                for c in cliques(set(), 0, u, degree, degree, graph, seen):
                    return ','.join([vertex_lookup[v] for v in sorted(c)])

def mogrify(line):
    return line.split('-')

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = [line.rstrip('\n') for line in f]

    data = list(map(mogrify, lines))

    print('part 1:', part1(data))
    print('part 2:', part2(data))

if __name__ == '__main__':
    main()
