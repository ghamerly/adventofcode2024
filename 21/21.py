#!/usr/bin/env python3

# https://adventofcode.com/2024/day/21 - "Keypad Conundrum"
# Author: Greg Hamerly

# Part 2 for this one took me way too long.

import sys
import itertools

DIRECTION = {'>': ( 0,  1),
             '<': ( 0, -1),
             '^': (-1,  0),
             'v': ( 1,  0)}

NUMERIC_KEYPAD = ['789',
                  '456',
                  '123',
                  'X0A']

DIRECTION_KEYPAD = ['X^A',
                    '<v>']

NUMERIC_POSITIONS = {
        col: (r, c) for r, row in enumerate(NUMERIC_KEYPAD)
        for c, col in enumerate(row) }

DIRECTION_POSITIONS = {
        col: (r, c) for r, row in enumerate(DIRECTION_KEYPAD)
        for c, col in enumerate(row) }

def num_direction_changes(path):
    '''We know it's possible to change directions at most once, and that leads
    to shorter paths, so this function helps us know how many directional
    changes we have made, for pruning.'''
    prev = None
    changes = 0
    directions = ''.join([d for _, _, d in path])
    for d in directions:
        if prev is not None:
            if prev != d:
                changes += 1
        prev = d
    return changes

def find_shortest_paths(keypad, r1, c1, r2, c2):
    '''Generate all shortest paths on the given keypad from (r1,c1) to (r2,c2)
    that:
        - are the shortest (least number of steps)
        - stay on the keypad (and avoid the 'X')
        - have at most one change in direction
        '''

    frontier = [[(r1, c1, '')]]
    cost = {(r1, c1): 0}
    oo = 1e100

    if (r1, c1) == (r2, c2):
        yield ''
        return

    while frontier:
        new_frontier = []
        for path in frontier:
            r1, c1, _ = path[-1]
            for d, (dr, dc) in DIRECTION.items():
                r = r1 + dr
                c = c1 + dc
                if (0 <= r < len(keypad)) and (0 <= c < len(keypad[r])) and \
                        (keypad[r][c] != 'X') and (cost[(r1, c1)] + 1 <= cost.get((r, c), oo)):
                    p = path + [(r, c, d)]

                    # prune paths that change direction more than once
                    if num_direction_changes(p) > 1:
                        continue

                    if (r, c) == (r2, c2):
                        yield ''.join([dd for _, _, dd in p])
                    else:
                        new_frontier.append(p)

                    cost[(r, c)] = cost[(r1, c1)] + 1

        frontier = new_frontier


#def simulate(path, r, c, keypad):
#    '''For debugging.'''
#    output = []
#    visited_before_A = set()
#    for pi in path:
#        if r < 0 or r >= len(keypad):
#            return None
#        if c < 0 or c >= len(keypad[r]):
#            return None
#        if keypad[r][c] == 'X':
#            return None
#
#        if (r, c) in visited_before_A:
#            return None
#
#        visited_before_A.add((r, c))
#
#        if pi == 'A':
#            output.append(keypad[r][c])
#            visited_before_A = set()
#        else:
#            r += DIRECTION[pi][0]
#            c += DIRECTION[pi][1]
#
#    return ''.join(output)


#########################################
# This was how I initially solved part 1
#def find_possibilities(positions, keypad, sequence):
#    possibilities = [[] for _ in range(len(sequence) - 1)]
#    for i in range(1, len(sequence)):
#        r1, c1 = positions[sequence[i-1]]
#        r2, c2 = positions[sequence[i]]
#        for p in find_shortest_paths(keypad, r1, c1, r2, c2):
#            possibilities[i-1].append(p)
#    return possibilities
#
#def part1(data):
#    ans = 0
#    for line in data:
#        shortest = 1e100
#        p0 = find_possibilities(NUMERIC_POSITIONS, NUMERIC_KEYPAD, 'A' + line)
#
#        for fp0 in itertools.product(*p0):
#            fp0 = 'A'.join(fp0) + 'A'
#            p1 = find_possibilities(DIRECTION_POSITIONS, DIRECTION_KEYPAD, 'A' + fp0)
#
#            for fp1 in itertools.product(*p1):
#                fp1 = 'A'.join(fp1) + 'A'
#                p2 = find_possibilities(DIRECTION_POSITIONS, DIRECTION_KEYPAD, 'A' + fp1)
#
#                for fp2 in itertools.product(*p2):
#                    fp2 = 'A'.join(fp2) + 'A'
#                    shortest = min(shortest, len(fp2))
#        ans += int(line[:-1]) * shortest
#
#    return ans
#########################################

def shortest_rec2(src, dest, remaining_depth, cache):
    '''Return the length of the shortest keystroke sequence that gets from src
    to depth at the given depth in the recursion. We are working our way from
    the "bottom" to the "top" of the recursion (from the numeric keypad that is
    receiving direction, towards the directional keypads giving directions, with
    the human at remaining_depth=0).'''

    if remaining_depth == 0:
        #print(f'{indent}bottoming out')
        return 1 # the dest key itself

    key = (src, dest, remaining_depth)

    if key not in cache:
        shortest = 1e100

        # we may have multiple ways of getting from src to dest; try all of them
        for p in find_shortest_paths(DIRECTION_KEYPAD, *DIRECTION_POSITIONS[src],
                                     *DIRECTION_POSITIONS[dest]):
            # since we are not at the "top" of the recursion (the human keypad),
            # we must start at 'A'
            prev = 'A'
            l = 0
            for pi in p:
                l += shortest_rec2(prev, pi, remaining_depth - 1, cache)
                prev = pi
            # we must send the command 'A' to tell the next lowest level to push
            # the button
            l += shortest_rec2(prev, 'A', remaining_depth - 1, cache)
            shortest = min(shortest, l)

        cache[key] = shortest

    return cache[key]

def solve(data, depth):
    '''This is the top of the recursion, but the innermost keypad (the numeric
    keypad). For each numeric code, recursively find the shortest sequence with
    memoization.'''

    ans = 0

    # the cache + memoization is key to making it fast, though the cache does
    # not grow very large (474 entries for part 2)
    cache = {}

    for line in data:

        # we start on symbol 'A' on the numeric keypad, always
        xprev = 'A'

        # this accumulates the length of the shortest path over the whole
        # sequence
        line_shortest = 0

        # go over every pair of adjacent symbols in the line (starting with 'A',
        # in xprev)
        for xcurr in line:

            # Between xprev and xcurr, there may be multiple options. Try all of
            # them and keep the shortest.
            shortest = 1e100
            for p in find_shortest_paths(NUMERIC_KEYPAD, *NUMERIC_POSITIONS[xprev],
                                         *NUMERIC_POSITIONS[xcurr]):

                l = 0
                prev = 'A' # start at 'A'
                for pi in p:
                    l += shortest_rec2(prev, pi, depth, cache)
                    prev = pi
                # send the signal to push the button
                l += shortest_rec2(prev, 'A', depth, cache)

                shortest = min(shortest, l)

            # from xcurr to xprev, we now know the shortest path; add it to the
            # length of our solution for this line
            line_shortest += shortest
            xprev = xcurr

        # this is the formula given in the problem - length of the shortest
        # sequence of keystrokes (of the human-directed directional keypad)
        # times the number represented by the first three integers in the line
        ans += int(line[:-1]) * line_shortest

    #print(f'{len(cache)=}')

    return ans

def part1(data):
    # for part 1, there are 2 intermediate robot directional keypads
    return solve(data, 2)

def part2(data):
    # for part 2, there are 25 intermediate robot directional keypads
    return solve(data, 25)

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
