#!/usr/bin/env python3

# https://adventofcode.com/2024/day/2 - "Red-Nosed Reports"
# Author: Greg Hamerly

import sys

def safe(row):
    if not (row in [sorted(row), sorted(row, reverse=True)]):
        return False
    for i in range(1, len(row)):
        if not 1 <= abs(row[i] - row[i-1]) <= 3:
            return False
    return True            

def part1(data):
    """Abuse the fact that Python allows us to sum booleans as integers."""
    return sum(map(safe, data))

def part2(data):
    """I do not love the inefficiency of this."""
    s = 0
    for row in data:
        if safe(row):
            s += 1
        else:
            for i in range(len(data)):
                r = row[:i] + row[i+1:]
                if safe(r):
                    s += 1
                    break
    return s

def mogrify(line):
    return list(map(int, line.split()))

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
