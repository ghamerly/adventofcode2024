#!/usr/bin/env python3

# https://adventofcode.com/2024/day/5 - "Print Queue"
# Author: Greg Hamerly

import sys
import functools

class Graph:
    def __init__(self):
        self.less_than = {}

    def add_constraint(self, a, b):
        for x in [a, b]:
            if x not in self.less_than:
                self.less_than[x] = set()
        self.less_than[a].add(b)

    def less_than_cmp(self, a, b):
        if b in self.less_than[a]:
            return -1
        if a in self.less_than[b]:
            return 1
        # the data from the problem seems to have a constraint between every
        # pair of numbers - this is a total ordering
        assert False

def solve(data, extract_answer):
    constraints = [c for desc, c in data if desc == 'constraint']
    orders = [c for desc, c in data if desc == 'order']

    g = Graph()
    for a, b in constraints:
        g.add_constraint(a, b)

    ans = 0
    for o in orders:
        assert len(o) % 2 == 1
        o2 = sorted(o, key=functools.cmp_to_key(g.less_than_cmp))
        ans += extract_answer(o, o2)

    return ans

def part1(data):
    def extract_answer(o, o2):
        return o[len(o) // 2] if o == o2 else 0
    return solve(data, extract_answer)

def part2(data):
    def extract_answer(o, o2):
        return o2[len(o2) // 2] if o != o2 else 0
    return solve(data, extract_answer)

def mogrify(line):
    if '|' in line:
        return 'constraint', list(map(int, line.split('|')))
    elif ',' in line:
        return 'order', list(map(int, line.split(',')))
    else:
        return 'blank', []

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
