#!/usr/bin/env python3

# https://adventofcode.com/2024/day/14 - "Restroom Redoubt"
# Author: Greg Hamerly

import re
import sys
import time

def part1(data, width=101, height=103, seconds=100):
    #width = 11
    #height = 7
    locations = {}

    def quadrant(x, y):
        if x * 2 + 1 == width or y * 2 + 1 == height:
            return None
        offset = 0 if y * 2 < height else 2
        return offset if x * 2 < width else 1 + offset

    quadrant_count = {}
    for x, y, dx, dy in data:
        x = (x + seconds * dx) % width
        y = (y + seconds * dy) % height
        locations[(x, y)] = locations.get((x, y), 0) + 1
        q = quadrant(x, y)
        if q is not None:
            quadrant_count[q] = quadrant_count.get(q, 0) + 1

    if False:
        for y in range(height):
            out = []
            for x in range(width):
                if quadrant(x, y) is None:
                    out.append(' ')
                else:
                    out.append(locations.get((x, y), '.'))

            print(' '.join(map(str, out)))

    ans = 1
    for m in quadrant_count.values():
        ans *= m
    return ans


def part2(data):
    width = 101
    height = 103

    s = 0
    while True:
        locations = {}
        count = [0] * height
        for x, y, dx, dy in data:
            x = (x + s * dx) % width
            y = (y + s * dy) % height
            count[y] += 1
            locations[(x, y)] = locations.get((x, y), 0) + 1

        # heuristic: if none of the robots overlap, stop and inspect
        if max(locations.values()) == 1:
            print(count)

            print('=' * 150)
            print(s)
            for y in range(height):
                out = [locations.get((x, y), '.') for x in range(width)]
                print(''.join(map(str, out)))

            return s

        s += 1


def mogrify(line):
    p = re.compile('p=([-0-9]+),([-0-9]+) v=([-0-9]+),([-0-9]+)')
    return list(map(int, p.match(line).groups()))

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
