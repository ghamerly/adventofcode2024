#!/usr/bin/env python3

# https://adventofcode.com/2024/day/9 - "Disk Fragmenter"
# Author: Greg Hamerly

import sys

def map_data(data):
    assert len(data) == 1
    data = data[0]
    n = sum(data)

    # put the data into the original layout, into "m"
    m = [None] * n
    p = 0 # position
    for i, l in enumerate(data):
        if i % 2 == 0:
            for j in range(l):
                m[p + j] = i // 2
        p += l
    assert p == n

    return m, n

def checksum(m):
    cksum = 0
    for i, v in enumerate(m):
        if v is not None:
            cksum += i * v
    return cksum

def part1(data):
    m, n = map_data(data)

    end = n - 1
    start = 0
    while start < end:
        while start < end and m[start] is not None:
            start += 1
        while start < end and m[end] is None:
            end -= 1
        if start < end:
            assert m[start] is None
            assert m[end] is not None
            m[start] = m[end]
            m[end] = None
            start += 1
            end -= 1

    return checksum(m)

def part2(data):
    m, n = map_data(data)

    # find_first_gap() finds the earliest gap that is at least as large as the
    # given size. We use last_gap_of_size to remember where you were last time
    # you went looking for a gap of a certain size; we start searching again
    # from there. This is the key to speeding up this search significantly.
    last_gap_of_size = {}
    def find_first_gap(size):
        start = last_gap_of_size.get(size, 0)

        for i in range(start, n - size):
            if all([x is None for x in m[i:i+size]]):
                last_gap_of_size[size] = i
                return i

        # we reached the end, there are no more gaps of this size
        last_gap_of_size[size] = n

    # helper function to find the beginning index of a block ending at end
    def block_start(end):
        start = end
        while 0 < start and m[start-1] == m[end]:
            start -= 1
        return start

    # work from the back to front and move blocks as we can
    end = n - 1
    while end >= 0:
        start = block_start(end)
        gap_start = find_first_gap(end-start+1)
        if gap_start is not None and gap_start < start:
            for i in range(end - start + 1):
                m[gap_start + i] = m[start + i]
                m[start + i] = None
        end = start - 1

    return checksum(m)

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
