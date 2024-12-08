#!/usr/bin/env python3

# https://adventofcode.com/2024/day/8 - "Resonant Collinearity"
# Author: Greg Hamerly

import sys

def output(data, antinodes):
    for r, row in enumerate(data):
        out_row = []
        for c, col in enumerate(row):
            out_row.append('#' if (r, c) in antinodes else col)
        print(''.join(out_row))

def solve(data, min_multiplier, max_multiplier):
    antennas = {}
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            if col != '.':
                if col not in antennas:
                    antennas[col] = set()
                antennas[col].add((r, c))

    antinodes = set()
    for a in antennas:
        for r1, c1 in antennas[a]:
            for r2, c2 in antennas[a]:
                if (r1, c1) == (r2, c2):
                    continue
                dr = r2 - r1
                dc = c2 - c1

                for m in range(min_multiplier, max_multiplier + 1):
                    in_bounds = False
                    for r, c in [(r1 - m * dr, c1 - m * dc), (r2 + m * dr, c2 + m * dc)]:
                        if 0 <= r < len(data) and 0 <= c < len(data[r]):
                            in_bounds = True
                            antinodes.add((r, c))
                    if not in_bounds:
                        break

    #output(data, antinodes)

    return len(antinodes)

def part1(data):
    return solve(data, 1, 1)

def part2(data):
    return solve(data, 0, 1000)

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
