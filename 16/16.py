#!/usr/bin/env python3

# https://adventofcode.com/2024/day/16 - "Reindeer Maze"
# Author: Greg Hamerly

import heapq
import sys

def find_all_costs(data):
    walls = set()
    position = target = None
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            match col:
                case '#': walls.add((r, c))
                case 'S': start = (r, c)
                case 'E': target = (r, c)
                case '.': pass
                case _: assert False, row

    position = start
    frontier = [(0, '>', *position)]
    best_cost = {('>', *position): 0}
    # (direction, position) -> (direction, previous position)
    incoming_links = {('>', *position): set()}

    move = {'>': ( 0, 1),
            '<': ( 0,-1),
            '^': (-1, 0),
            'v': ( 1, 0)}

    turn_cost = {'>': {'^': 1000, 'v': 1000, '<': 2000},
                 '<': {'^': 1000, 'v': 1000, '>': 2000},
                 '^': {'<': 1000, '>': 1000, 'v': 2000},
                 'v': {'<': 1000, '>': 1000, '^': 2000}}

    oo = 1e100

    while frontier:
        cost, current_dir, r, c = heapq.heappop(frontier)

        for new_dir, tc in turn_cost[current_dir].items():
            new_cost = cost + tc
            k = (new_dir, r, c)
            if new_cost < best_cost.get(k, oo):
                best_cost[k] = new_cost
                heapq.heappush(frontier, (new_cost, *k))
                incoming_links[k] = {(current_dir, r, c)}

        dr, dc = move[current_dir]
        new_position = (r + dr, c + dc)
        if new_position not in walls:
            k = (current_dir, *new_position)
            if cost + 1 < best_cost.get(k, oo):
                best_cost[k] = cost + 1
                heapq.heappush(frontier, (cost + 1, *k))
                incoming_links[k] = {(current_dir, r, c)}
            elif cost + 1 == best_cost[k]:
                incoming_links[k].add((current_dir, r, c))
                assert new_position not in incoming_links.get((current_dir, r, c), set())

    # debugging...
    for p1 in incoming_links:
        for p2 in incoming_links[p1]:
            if p1 in incoming_links[p2]:
                print('ERROR')
                print(p1, incoming_links[p1])
                print(p2, incoming_links[p2])
                assert False

    return start, target, best_cost, incoming_links

def part1(data):
    _, target, best_cost, _ = find_all_costs(data)
    return min([best_cost.get((d, *target)) for d in '^v<>'])

def part2(data):
    start, target, best_cost, incoming_links = find_all_costs(data)

    # trace backwards from the target, keeping track of all paths that could
    # have led us to each position (with direction) by the shortest route
    best = min([best_cost.get((d, *target)) for d in '^v<>'])
    on_shortest_path = {(d, *target) for d in '^v<>' if best_cost.get((d, *target)) == best}
    frontier = set(on_shortest_path)
    while frontier:
        new_frontier = set()
        for p in frontier:
            i = incoming_links[p]
            on_shortest_path.update(i)
            new_frontier.update(i)

        frontier = new_frontier

    # we have positions with directions, but we only need positions
    shortest_path_positions = {(r, c) for (_, r, c) in on_shortest_path}
    return len(shortest_path_positions)

def mogrify(line):
    return line

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
