#!/usr/bin/env python3

# https://adventofcode.com/2024/day/7 - "Bridge Repair"
# Author: Greg Hamerly

import sys

def all_combos(ops, n, ans=None):
    if ans is None:
        ans = [None] * n

    if n == 0:
        yield ans
    else:
        for o in ops:
            ans[n-1] = o
            yield from all_combos(ops, n - 1, ans)

def possible(eqn, possible_operators):
    target, *terms = eqn

    for ops in all_combos(possible_operators, len(terms) - 1):
        r = terms[0]
        for op, t in zip(ops, terms[1:]):
            if op == '+':
                r += t
            elif op == '*':
                r *= t
            elif op == '|':
                r = int(str(r) + str(t))
            else:
                assert False, f'what is operator {op}?'

            if r > target:
                break

        if r == target:
            return True

    return False

def solve(data, possible_operators):
    answer = 0
    for eqn in data:
        if possible(eqn, possible_operators):
            answer += eqn[0]
    return answer

def part1(data):
    return solve(data, '*+')

def part2(data):
    return solve(data, '*+|')

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
