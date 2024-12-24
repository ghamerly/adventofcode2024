#!/usr/bin/env python3

# https://adventofcode.com/2024/day/22 - "Monkey Market"
# Author: Greg Hamerly

import collections
import sys

PRUNE_MODULUS = 16777216

def calculate(x, iterations):
    all_iterations = [x]
    for _ in range(iterations):
        x = (x ^ (x * 64)) % PRUNE_MODULUS
        x = (x ^ (x // 32)) % PRUNE_MODULUS
        x = (x ^ (x * 2048)) % PRUNE_MODULUS
        all_iterations.append(x)

    return all_iterations

def part1(data):
    ans = 0
    for x in data:
        ans += calculate(x, 2000)[-1]
    return ans

def part2(data):
    signatures = {} # signature => sum of first price in each sequence
    for x in data:
        p = [z % 10 for z in calculate(x, 2000)]

        seen_this_sequence = set()

        s = collections.deque([p[i] - p[i-1] for i in range(3)])
        for i in range(4, len(p)):
            s.append(p[i] - p[i-1])
            k = tuple(s)
            if k not in seen_this_sequence:
                seen_this_sequence.add(k)
                signatures[k] = signatures.get(k, 0) + p[i]
            s.popleft()

    return max(signatures.values())

def mogrify(line):
    return int(line)

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
