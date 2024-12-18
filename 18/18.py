#!/usr/bin/env python3

# https://adventofcode.com/2024/day/18 - "RAM Run"
# Author: Greg Hamerly

import sys

def display(max_coord, walls, dists):
    for y in range(max_coord + 1):
        row = []
        for x in range(max_coord + 1):
            if (y, x) in walls:
                row.append('#')
            elif (y, x) in dists:
                row.append(str(dists[(y, x)] % 10))
            else:
                row.append('.')
        print(''.join(row))

def simulate(data, max_coord):
    walls = {(y, x) for (x, y) in data}
    #print(f'{walls=}')
    in_bounds = lambda xy: (0 <= xy[0] <= max_coord) and (0 <= xy[1] <= max_coord)

    #display(max_coord, walls, {})

    dist = {(0, 0): 0}
    frontier = [(0, 0)]
    while frontier:
        #print(f'{frontier=}')
        next_frontier = []
        for y, x in frontier:
            for neighbor in [(y,x-1), (y,x+1), (y-1,x), (y+1,x)]:
                if in_bounds(neighbor) and (neighbor not in walls) and (neighbor not in dist):
                    dist[neighbor] = dist[(y, x)] + 1
                    next_frontier.append(neighbor)
        frontier = next_frontier

    #print(f'{dist=}')

    return dist.get((max_coord, max_coord))


def part1(data):
    return simulate(data[:1024], 70)

def part2(data):
    low = 0
    high = len(data)

    while low < high:
        mid = (low + high) // 2
        #print(f'{low=} {mid=} {high=}')
        if simulate(data[:mid], 70) is None:
            high = mid
        else:
            low = mid + 1
    return ','.join(map(str, data[mid-1]))

def mogrify(line):
    return tuple(map(int, line.split(',')))

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
