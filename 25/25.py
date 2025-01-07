#!/usr/bin/env python3

# https://adventofcode.com/2024/day/25 - "Code Chronicle"
# Author: Greg Hamerly

# Part 2 is not done (I haven't finished all the other stars yet)

import sys

def heights(kl):
    kl = zip(*kl)
    return [l.count('#') - 1 for l in kl]

def part1(data):
    keys = []
    locks = []

    for i in range(0, len(data), 8):
        kl = data[i:i+7]
        if '.' in kl[0]: # lock
            assert '.' not in kl[-1]
            locks.append(heights(kl))
        else: # key
            assert '.' in kl[-1]
            keys.append(heights(kl[::-1]))

    ans = 0
    for k in keys:
        for l in locks:
            if max([(a + b) for a, b in zip(k, l)]) < 6:
                ans += 1
    return ans

def part2(data):
    # cannot get this last part of the puzzle without finishing the other stars
    for x in data:
        pass

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
