#!/usr/bin/env python3

# https://adventofcode.com/2024/day/10 - "Hoof It"
# Author: Greg Hamerly

import sys

def solve(data):
    # BFS starting from each trailhead, keeping track of the trailheads and
    # number of paths as we go.
    TRAILHEAD = 0
    DESTINATION = 9
    trailheads = []
    for r, row in enumerate(data):
        trailheads.extend([(r, c) for c, col in enumerate(row) if col == TRAILHEAD])

    # answer keeps for each trailhead a dictionary of {destination: path_count}
    answer = {t: {} for t in trailheads}
    queue = {t: {t: 1} for t in trailheads}
    while queue:
        next_queue = {}
        for r, c in queue:
            if data[r][c] == DESTINATION:
                for th, count in queue[(r, c)].items():
                    if (r, c) not in answer[th]:
                        answer[th][(r, c)] = 0
                    answer[th][(r, c)] += count
            for rr, cc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
                if 0 <= rr < len(data) and 0 <= cc < len(data[rr]):
                    if data[r][c] + 1 == data[rr][cc]:
                        if (rr, cc) not in next_queue:
                            next_queue[(rr, cc)] = {}
                        for th, count in queue[(r, c)].items():
                            if th not in next_queue[(rr, cc)]:
                                next_queue[(rr, cc)][th] = 0
                            next_queue[(rr, cc)][th] += count
        queue = next_queue

    return answer

def part1(data):
    answer = solve(data)
    return sum(map(len, answer.values()))

def part2(data):
    answer = solve(data)
    return sum([sum(dests.values()) for th, dests in answer.items()])

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
