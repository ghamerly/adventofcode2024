#!/usr/bin/env python3

# https://adventofcode.com/2024/day/1 - "Historian Hysteria"
# Author: Greg Hamerly

import sys

def part1(data):
    col1 = sorted([x for x, y in data])
    col2 = sorted([y for x, y in data])
    return sum(map(abs, [x - y for x, y in zip(col1, col2)]))

def part2(data):
    col1 = [x for x, y in data]
    col2 = [y for x, y in data]
    s = 0
    for x in col1:
        s += x * col2.count(x)
    return s

def mogrify(line):
    return tuple(map(int, line.split()))

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
