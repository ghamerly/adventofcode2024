#!/usr/bin/env python3

# https://adventofcode.com/2024/day/10 - "Hoof It"
# Author: Greg Hamerly

import sys

def part1(data):
    trailheads = {}
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            if col == 0:
                trailheads[(r, c)] = set()

    answer = {t: set() for t in trailheads}
    queue = {t: {t} for t in trailheads}
    while queue:
        next_queue = {}
        for r, c in queue:
            h = data[r][c]
            if h == 9:
                for th in queue[(r, c)]:
                    answer[th].add((r, c))
            for rr, cc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
                if 0 <= rr < len(data) and 0 <= cc < len(data[rr]):
                    h2 = data[rr][cc]
                    if h + 1 == h2:
                        if (rr, cc) not in next_queue:
                            next_queue[(rr, cc)] = set()
                        next_queue[(rr, cc)].update(queue[(r, c)])
        queue = next_queue

    return sum(map(len, answer.values()))

def part2(data):
    trailheads = {}
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            if col == 0:
                trailheads[(r, c)] = set()

    answer = {t: 0 for t in trailheads}
    queue = {t: {t: 1} for t in trailheads}
    while queue:
        next_queue = {}
        for r, c in queue:
            h = data[r][c]
            if h == 9:
                for th, count in queue[(r, c)].items():
                    answer[th] += count
            for rr, cc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
                if 0 <= rr < len(data) and 0 <= cc < len(data[rr]):
                    h2 = data[rr][cc]
                    if h + 1 == h2:
                        if (rr, cc) not in next_queue:
                            next_queue[(rr, cc)] = {}
                        for th, count in queue[(r, c)].items():
                            if th not in next_queue[(rr, cc)]:
                                next_queue[(rr, cc)][th] = 0
                            next_queue[(rr, cc)][th] += count
        queue = next_queue

    return sum(answer.values())

def mogrify(line):
    return list(map(int, line))

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
