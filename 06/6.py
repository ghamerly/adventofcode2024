#!/usr/bin/env python3

# https://adventofcode.com/2024/day/6 - "Guard Gallivant"
# Author: Greg Hamerly

import sys

def simulate(start, rows, cols, blocks):
    def in_grid(r, c):
        if r < 0 or rows <= r:
            return False
        if c < 0 or cols <= c:
            return False
        return True

    loc = start
    direction = (-1, 0) # assuming up to begin
    visited = {}
    while in_grid(*loc):
        if loc not in visited:
            visited[loc] = set()

        if direction in visited[loc]:
            return 'loop', visited

        visited[loc].add(direction)
        r, c = (loc[0] + direction[0], loc[1] + direction[1])
        if (r, c) in blocks:
            direction = (direction[1], -direction[0])
        else:
            loc = (r, c)

    return 'exit', visited

def prepare(data):
    blocks = set()
    start = None
    for r in range(len(data)):
        for c in range(len(data[r])):
            if data[r][c] == '#':
                blocks.add((r, c))
            elif data[r][c] == '^':
                start = (r, c)
    return start, blocks

def part1(data):
    start, blocks = prepare(data)

    _, visited = simulate(start, len(data), len(data[0]), blocks)

    return len(visited)

def part2(data):
    start, blocks = prepare(data)

    rows, cols = len(data), len(data[0])

    _, possible = simulate(start, rows, cols, blocks)

    # this could be optimized so much...
    answer = 0
    for rc in possible:
        assert rc not in blocks
        if rc == start:
            continue

        blocks.add(rc)
        result, _ = simulate(start, rows, cols, blocks)
        blocks.remove(rc)

        if result == 'loop':
            answer += 1

    return answer

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
