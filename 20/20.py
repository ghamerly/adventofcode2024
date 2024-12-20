#!/usr/bin/env python3

# https://adventofcode.com/2024/day/20 - "Race Condition"
# Author: Greg Hamerly

import sys

def bfs(start_loc, walls):
    frontier = [start_loc]
    dist = {start_loc: 0}
    while frontier:
        next_frontier = set()
        for r, c in frontier:
            for neighbor in [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]:
                if neighbor in walls:
                    continue
                if neighbor in dist:
                    continue
                next_frontier.add(neighbor)
                dist[neighbor] = dist[(r, c)] + 1
        frontier = next_frontier
    return dist

def solve(data, max_offset):
    walls = {(r, c) for r, row in enumerate(data) for c, col in enumerate(row) if col == '#'}
    start = [(r, c) for r, row in enumerate(data) for c, col in enumerate(row) if col == 'S'][0]
    end = [(r, c) for r, row in enumerate(data) for c, col in enumerate(row) if col == 'E'][0]

    dist_forward = bfs(start, walls)
    dist_backward = bfs(end, walls)

    cheats = set()
    #cheats_of_size = {} # for comparison with the problem description
    total_dist = dist_forward[end]
    for (r, c), df in dist_forward.items():
        for offset in range(1, max_offset + 1):
            for dr in range(offset + 1):
                dc = offset - dr
                assert dr + dc == offset
                for neighbor in [(r+dr,c+dc), (r-dr,c+dc), (r+dr,c-dc), (r-dr,c-dc)]:
                    if neighbor not in dist_backward:
                        continue

                    new_dist = df + dist_backward[neighbor] + offset
                    savings = total_dist - new_dist
                    if savings >= 100:
                        cheats.add((r, c) + neighbor)
                        #cheats_of_size[savings] = cheats_of_size.get(savings, 0) + 1

    #for savings, num in sorted(cheats_of_size.items()):
        #print(num, savings)

    return len(cheats)

def part1(data):
    return solve(data, 2)

def part2(data):
    return solve(data, 20)

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
