#!/usr/bin/env python3

# https://adventofcode.com/2024/day/19 - "Linen Layout"
# Author: Greg Hamerly

import sys

def solve_recursive(patterns, target, start, count=None):
    if count is None:
        count = {} # start => number of ways that we can solve target[start:]

    if start == len(target):
        return 1

    if start not in count:
        count[start] = 0
        for end in range(start + 1, len(target) + 1):
            t = target[start:end]
            if target[start:end] in patterns:
                sub_count = solve_recursive(patterns, target, end, count)
                count[start] += sub_count

    return count[start]

def solve(data, combiner):
    patterns = set(data[0].split(', '))
    targets = data[2:]

    ans = 0
    for t in targets:
        ans += combiner(solve_recursive(patterns, t, 0))

    return ans
    
def part1(data):
    return solve(data, lambda x: 1 if x else 0)

def part2(data):
    return solve(data, lambda x: x)

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
