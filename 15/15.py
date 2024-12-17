#!/usr/bin/env python3

# https://adventofcode.com/2024/day/15 - "Warehouse Woes"
# Author: Greg Hamerly
#
# Not proud of this one.

import sys

def push1(grid, r, c, dr, dc):
    if grid[r][c] == '#':
        return False
    ans = (grid[r][c] == '.') or push1(grid, r + dr, c + dc, dr, dc)
    if ans:
        grid[r][c] = grid[r - dr][c - dc]
    return ans

def display(grid):
    print('-' * 20)
    print('    ' + ''.join([f'{c%10}' for c in range(len(grid[0]))]))
    for r, row in enumerate(grid):
        print(f'{r:3} ' + ''.join(row))
    print('-' * 20)

def part1(data):
    grid = []
    directions = []
    dest = grid
    for line in data:
        if line:
            dest.append(line)
        else:
            dest = directions
    directions = ''.join(directions)
    for r in range(len(grid)):
        grid[r] = list(grid[r])

    robot = None
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == '@':
                robot = (r, c)
                break
        if robot is not None:
            break

    deltas = { '^': (-1, 0), '>': (0,  1), 'v': (1,  0), '<': (0, -1) }

    r, c = robot
    for d in directions:
        dr, dc = deltas[d]
        if push1(grid, r, c, dr, dc):
            grid[r][c] = '.'
            r += dr
            c += dc
        #display(grid)

    ans = 0
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == 'O':
                ans += r * 100 + c

    return ans

class Block:
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def hits(self, r, c):
        return r == self.r and c in (self.c, self.c + 1)

    def as_tuple(self):
        return (self.r, self.c)

    def __hash__(self):
        return hash(self.as_tuple())

    def __eq__(self, b):
        return self.as_tuple() == b.as_tuple()
    
    def __repr__(self):
        return repr(self.as_tuple())

    def move(self, dr, dc):
        return Block(self.r + dr, self.c + dc)

    def blocks_overlap(self, b):
        return self.hits(b.r, b.c) or self.hits(b.r, b.c + 1)

def would_hit_block(r, c, dr, dc, blocks):
    for b in blocks:
        if b.hits(r + dr, c + dc):
            return b
    return False

def push2(blocks, dr, dc, all_blocks, walls):
    if not blocks:
        return True

    assert blocks <= all_blocks

    blocks_hit = set()
    for b in blocks:
        m = b.move(dr, dc)
        if any([m.hits(*w) for w in walls]):
            return False

        for a in all_blocks:
            if a == b:
                continue
            if m.blocks_overlap(a):
                blocks_hit.add(a)

    if push2(blocks_hit, dr, dc, all_blocks, walls):
        for b in blocks:
            all_blocks.remove(b)
        all_blocks.update({b.move(dr, dc) for b in blocks})

        return True

    return False

def part2(data):
    grid = []
    directions = []
    dest = grid
    for line in data:
        if line:
            dest.append(line)
        else:
            dest = directions
    directions = ''.join(directions)

    m = { '#': '##', 'O': '[]', '.': '..', '@': '@.' }
    for r in range(len(grid)):
        grid[r] = list(''.join([m[c] for c in grid[r]]))

    walls = set()
    blocks = set()
    robot = None
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == '@':
                robot = (r, c)
            elif col == '#':
                walls.add((r, c))
            elif col == '[':
                blocks.add(Block(r, c))

    deltas = { '^': (-1, 0), '>': (0,  1), 'v': (1,  0), '<': (0, -1) }

    #print('START')
    #display2(walls, blocks, robot)

    r, c = robot
    for i, d in enumerate(directions):
        dr, dc = deltas[d]
        if (r + dr, c + dc) not in walls:
            b = would_hit_block(r, c, dr, dc, blocks)
            if b:
                if push2({b}, dr, dc, blocks, walls):
                    r += dr
                    c += dc
            else:
                r += dr
                c += dc
        #print(f'AFTER INSTRUCTION {i} DIRECTION {d}')
        #display2(walls, blocks, (r, c))

    ans = 0
    for b in blocks:
        ans += b.r * 100 + b.c
    return ans

def display2(walls, blocks, robot):
    max_r = max([r for r, c in walls]) + 1
    max_c = max([c for r, c in walls]) + 1

    print('-' * 20)
    print('    ' + ''.join([f'{c%10}' for c in range(max_c)]))
    for r in range(max_r):
        row = []
        for c in range(max_c):
            if (r, c) == robot:
                row.append('@')
            elif Block(r, c) in blocks:
                row.append('[')
            elif Block(r, c - 1) in blocks:
                row.append(']')
            elif (r, c) in walls:
                row.append('#')
            else:
                row.append('.')
        print(f'{r:3} ' + ''.join(row))
    print('-' * 20)


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
