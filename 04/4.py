#!/usr/bin/env python3

# https://adventofcode.com/2024/day/4 - "Ceres Search"
# Author: Greg Hamerly

import sys

def find(grid, r, c, word, dr, dc):
    for i, w in enumerate(word):
        rr = r + dr * i
        cc = c + dc * i
        if rr < 0 or cc < 0 or rr >= len(grid) or cc >= len(grid[rr]):
            return False
        if grid[rr][cc] != w:
            return False
    return True

def part1(data):
    num_xmas = 0
    for r in range(len(data)):
        for c in range(len(data[r])):
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == dc == 0:
                        continue
                    if find(data, r, c, 'XMAS', dr, dc):
                        num_xmas += 1
    return num_xmas

def part2(data):
    num_crossed = 0
    for r in range(1, len(data) - 1):
        for c in range(1, len(data[r]) - 1):
            if data[r][c] != 'A':
                continue
            # a b c
            # d * e
            # f g h
            ah = ''.join(sorted(data[r-1][c-1] + data[r+1][c+1]))
            cf = ''.join(sorted(data[r-1][c+1] + data[r+1][c-1]))

            if ah == cf == 'MS':
                num_crossed += 1

    return num_crossed

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
