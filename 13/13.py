#!/usr/bin/env python3

# https://adventofcode.com/2024/day/13 - "Claw Contraption"
# Author: Greg Hamerly

import re
import sys

def solve_brute(ax, ay, bx, by, tx, ty):
    # try all possible combinations; this can solve part 1 but not part 2
    best_cost = None

    for ai in range(101):
        if ax * ai > tx or ay * ai > ty:
            break

        for bi in range(101):
            x = ax * ai + bx * bi
            y = ay * ai + by * bi
            if x > tx or y > ty:
                break
            if x == tx and y == ty:
                this_cost = ai * 3 + bi
                if best_cost is None:
                    best_cost = this_cost
                else:
                    best_cost = min(best_cost, this_cost)

    return best_cost

def solve_directly(ax, ay, bx, by, tx, ty):
    # We have these two starting equations, with unknowns ai and bi (the number
    # of times buttons a and b are pressed):
    #     tx = ai * ax + bi * bx (1)
    #     ty = ai * ay + bi * by (2)
    # we can solve for ai by rearranging equation (1):
    #   ai = (tx - bi * bx) / ax (3)
    # then plug in ai to equation (2):
    #   ty = (tx - bi * bx) * ay / ax + bi * by (4)
    # then do a bunch of algebra to solve for bi:
    #   bi = (ty * ax - tx * ay) / (ax * by - ay * bx) (5)
    # and we can use this to solve directly for bi, and then substitute back in
    # to (3) to solve for ai
    #
    # I realized that there's either 1 integer solution (given above), no
    # solution (if there is no integer solution), or infinite solutions (if the
    # three given vectors are collinear). That there is only one integer
    # solution (if it exists, and vectors are not collinear) can be seen as we
    # are adding together two vectors, defining two different slopes, to try to
    # leave the origin and hit a specified (tx, ty) point. If the two vectors
    # are not collinear, then there's only one way to do this, since the slopes
    # of the two vectors are different.
    #
    # 
    #  |        b
    #  |    z------- t
    #  |   /
    #  |  /
    #  | / a
    #  |/
    # -O---------------
    #  |
    #
    # here O is the origin, t is the target, a and b are vectors, and z is where
    # they intersect. Since we have two fixed endpoints (O and t), there's at
    # most exactly one way to do this when a and b are not collinear.

    num = ty * ax - tx * ay
    denom = ax * by - ay * bx
    if denom == 0: # collinear; just choose the lesser of a/b, if it's feasible
        assert False # but that doesn't occur in this problem, so skip it
    elif (num % denom) != 0:
        # there is no integer solution
        return None

    # solve for bi
    bi = num // denom

    if (tx - bi * bx) % ax:
        # there is no integer solution
        return None

    # solve for ai
    ai = (tx - bi * bx) // ax

    return ai * 3 + bi

def solve(data, offset=0):
    # get rid of empty lines
    data = list(filter(None, data))
    ans = 0
    for i in range(0, len(data), 3):
        ax, ay = map(int, data[i][1:])
        bx, by = map(int, data[i+1][1:])
        tx, ty = map(int, data[i+2])
        tx += offset
        ty += offset
        tokens = solve_directly(ax, ay, bx, by, tx, ty)
        if tokens is not None:
            ans += tokens
    return ans

def part1(data):
    return solve(data)

def part2(data):
    return solve(data, 10000000000000)

def mogrify(line):
    if not line: # skip empty lines
        return None

    button_pattern = re.compile('Button ([AB]): X[+]([0-9]+), Y[+]([0-9]+)')
    m = button_pattern.match(line)
    if m:
        return m.groups()

    prize_pattern = re.compile('Prize: X=([0-9]+), Y=([0-9]+)')
    return prize_pattern.match(line).groups()

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
