#!/usr/bin/env python3

# https://adventofcode.com/2024/day/3 - "Mull It Over"
# Author: Greg Hamerly

import re
import sys

def part1(data):
    pattern = re.compile(r'mul\(([0-9]+),([0-9]+)\)')
    s = 0
    for line in data:
        for m in pattern.finditer(line):
            a, b = map(int, m.groups())
            s += a * b
    return s

def part2(data):
    pattern = re.compile(r'mul\(([0-9]+),([0-9]+)\)|do\(\)|don\'t\(\)')
    s = 0
    state = True
    for line in data:
        for m in pattern.finditer(line):
            if 'mul' in m.group(0):
                a, b = map(int, m.groups())
                if state:
                    s += a * b
            elif 'don' in m.group(0):
                state = False
            else:
                state = True
    return s

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
