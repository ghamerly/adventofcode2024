#!/usr/bin/env python3

# https://adventofcode.com/2024/day/12 - "Garden Groups"
# Author: Greg Hamerly

import sys

def same_region_filter(r, c, grid):
    def _fltr(rr, cc):
        return (0 <= rr < len(grid)) \
                and (0 <= cc < len(grid[rr])) \
                and (grid[r][c] == grid[rr][cc])
    return _fltr

def neighbors(r, c, nbr_fltr=None):
    for rr, cc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
        if (nbr_fltr is None) or nbr_fltr(rr, cc):
            yield rr, cc

def perimeter(region):
    # one-liner
    # return len(region) * 4 - sum([(n in region) for rc in region for n in neighbors(*rc)])

    ans = len(region) * 4
    for rc in region:
        for n in neighbors(*rc):
            if n in region:
                ans -= 1

    return ans

def adjacent_sides(a, b):
    assert False
    return False

class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
    
    def find(self, x):
        assert 0 <= x < len(self.parent)
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        small = self.find(x)
        big = self.find(y)
        if small != big:
            if self.size[big] < self.size[small]:
                small, big = big, small
            self.size[big] += self.size[small]
            self.parent[small] = big

def num_sides(region):
    directions = {
            'BELOW': ( 1,  0),
            'ABOVE': (-1,  0),
            'RIGHT': ( 0,  1),
            'LEFT':  ( 0, -1)
            }

    def wall_neighbors(dr, dc):
        '''For a position with a wall, return offsets to the two neighbors that
        could share this wall.'''
        return [(-abs(dc), -abs(dr)), (abs(dc), abs(dr))]

    walls = {}
    for r, c in region:
        for direction, (dr, dc) in directions.items():
            if (r+dr, c+dc) not in region:
                k = (r, c, dr, dc)
                if k not in walls:
                    walls[k] = set()
                walls[k].add(direction)

    wall_id = {w: i for i, w in enumerate(walls)}

    ds = DisjointSet(len(walls))

    for wall_1 in walls:
        r, c, dr, dc = wall_1
        for ndr, ndc in wall_neighbors(dr, dc):
            wall_2 = (r+ndr, c+ndc, dr, dc)
            if wall_2 in walls:
                ds.union(wall_id[wall_1], wall_id[wall_2])

    unique_walls = {ds.find(x) for x in range(len(wall_id))}

    return len(unique_walls)

def floodfill_all(grid):
    plots = {} # plot_id => locations
    seen = set() # locations
    num_rows, num_cols = len(grid), len(grid[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if (r, c) in seen:
                continue
            frontier = [(r, c)]
            plot_id = (r, c, grid[r][c])
            plots[plot_id] = {(r, c)}
            seen.add((r, c))
            while frontier:
                new_frontier = []
                for rr, cc in frontier:
                    for n in neighbors(rr, cc, same_region_filter(rr, cc, grid)):
                        if n not in seen:
                            seen.add(n)
                            plots[plot_id].add(n)
                            new_frontier.append(n)
                frontier = new_frontier

    return plots

def part1(data):
    plots = floodfill_all(data)
    ans = 0
    for plot_id, region in plots.items():
        ans += len(region) * perimeter(region)
    return ans

def part2(data):
    plots = floodfill_all(data)
    ans = 0
    for plot_id, region in plots.items():
        ans += len(region) * num_sides(region)
    return ans

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
