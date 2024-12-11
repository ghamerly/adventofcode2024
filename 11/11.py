#!/usr/bin/env python3

# https://adventofcode.com/2024/day/11 - "Plutonian Pebbles"
# Author: Greg Hamerly

import sys

def solve(data, iterations):
    # one interesting feature of this problem is that after some number of
    # iterations, the set of keys in the frontier stops changing (only the
    # counts are changing). For the input I was given, there are 3811 keys. So
    # at that point, you could use a "repeated squaring" algorithm to fast
    # forward through the process of iteration.

    frontier = {x: data[0].count(x) for x in data[0]}
    for _ in range(iterations):
        next_frontier = {}
        for x, count in frontier.items():
            next_tokens = []
            if x == '0':
                next_tokens.append('1')
            elif len(x) % 2 == 0:
                next_tokens.extend([x[:len(x)//2], str(int(x[len(x)//2:]))])
            else:
                next_tokens.append(str(int(x) * 2024))

            for z in next_tokens:
                next_frontier[z] = next_frontier.get(z, 0) + count

        frontier = next_frontier

    # examine the data a bit
    #print(sorted(frontier.items(), key=lambda x: -x[1]))
    #print(len(frontier))

    return sum(frontier.values())

def part1(data):
    return solve(data, 25)

def part2(data):
    return solve(data, 75)

def mogrify(line):
    return line.split()

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
