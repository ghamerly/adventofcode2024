#!/usr/bin/env python3

# https://adventofcode.com/2024/day/7 - "Bridge Repair"
# Author: Greg Hamerly

import itertools
import sys

def part1(data):
    answer = 0

    for eqn in data:
        target, *terms = eqn

        p = len(terms) - 1
        for x in range(2 ** p):
            r = terms[0]
            for i, t in enumerate(terms[1:]):
                if x & (1 << i):
                    r *= t
                else:
                    r += t

            if r == target:
                answer += target
                break

    return answer

def all_combos(ops, n, ans=None):
    if ans is None:
        ans = []

    if n == 0:
        yield ans
        return

    ans.append(None)
    for o in ops:
        ans[-1] = o
        yield from all_combos(ops, n - 1, ans)
    ans.pop()
    

def part2(data):
    answer = 0

    for eqn in data:
        target, *terms = eqn

        p = len(terms) - 1
        found = False
        for ops in all_combos('+*|', p):
            #print('***', ops)
            r = terms[0]
            for op, t in zip(ops, terms[1:]):
                if op == '+':
                    r += t
                elif op == '*':
                    r *= t
                else:
                    r = int(str(r) + str(t))

                if r > target:
                    #print('breaking early')
                    break

            #print(p, eqn, ops, r)
            if r == target:
                #print(target, 'found it!')
                answer += target
                break

    return answer


def mogrify(line):
    return list(map(int, map(lambda s: s.strip(':'), line.split())))

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
