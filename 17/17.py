#!/usr/bin/env python3

# https://adventofcode.com/2024/day/17 - "Chronospatial Computer"
# Author: Greg Hamerly

# Part 2 is not done

import sys

class Impossible(Exception):
    def __init__(self, msg):
        super().__init__(msg)

def run_program(A, B, C, program, search=False):
    registers = [A, 0, 0]
    program = program[:]
    ip = 0
    output = []

    def combo_operand(o):
        if 0 <= o <= 3:
            return o
        assert o < 7
        return registers[o - 4]

    def adv(x):
        '''adv'''
        numerator = registers[0]
        denominator = 2 ** combo_operand(x)
        registers[0] = numerator // denominator

    def bxl(x):
        '''bxl'''
        registers[1] = registers[1] ^ x

    def bst(x):
        '''bst'''
        registers[1] = combo_operand(x) % 8

    def jnz(x):
        '''jnz'''
        nonlocal ip
        if registers[0] != 0:
            #print(f'jumping from {ip=} to {x=}')
            ip = x
            return False

    def bxc(x):
        '''bxc'''
        registers[1] = registers[1] ^ registers[2]

    def out(x):
        '''out'''
        nonlocal search
        o = combo_operand(x) % 8
        if search:
            if (output == len(program)) or (program[len(output)] != o):
                raise Impossible(output)
        output.append(o)

    def bdv(x):
        '''bdv'''
        numerator = registers[0]
        denominator = 2 ** combo_operand(x)
        registers[1] = numerator // denominator

    def cdv(x):
        '''cdv'''
        numerator = registers[0]
        denominator = 2 ** combo_operand(x)
        registers[2] = numerator // denominator
        #assert registers[2] == 0, (x, numerator, denominator, registers)

    opcodes = [ adv, bxl, bst, jnz, bxc, out, bdv, cdv ]

    while ip < len(program):
        assert ip + 1 < len(program)
       #if seen is not None:
       #    k = (ip, *registers)
       #    if k in seen:
       #        print(f'quitting with {k=}')
       #        raise Impossible([])
       #    seen.add(k)
        opcode = program[ip]
        operand = program[ip + 1]
        f = opcodes[opcode]
        #print(f'before: {ip=} {opcode=} {f=} {operand=} {registers=}')
        if f(operand) is not False:
            ip += 2
        #print(f'   after: {registers=}')

    #print(f'registers: {registers=}')

    #if (seen is not None) and output != program:
    if search and (output != program):
        raise Impossible(output)

    return output

def part1(data):
    output = run_program(*data)
    return ','.join(map(str, output))


# Here is a decompilation of the program:
#
#   2,4 = bst 4: reg[b] = reg[a] % 8                # b1 <- (a1 % 8)  -- lowest 3 bits of a into b
#   1,7 = bxl 7: reg[b] = reg[b] xor 7              # b2 <- b1 ^ 7 -- flip lowest 3 bits of b
#   7,5 = cdv 5: reg[c] = reg[a] // (2 ** reg[b])   # c1 <- a1 // (2 ** b2)
#   0,3 = adv 3: reg[a] = reg[a] // 8               # a2 <- a1 // 8 -- reduce a (loop counter)
#   1,7 = bxl 7: reg[b] = reg[b] xor 7              # b3 <- b2 ^ 7 == b1 flip lowest 3 bits of b (they are now the same as a's original lowest 3 bits?)
#   4,1 = bxc 1: reg[b] = reg[b] xor reg[c]         # b4 <- b3 ^ c1
#   5,5 = out 5: print(reg[b] % 8)                  # print(b4 % 8)
#   3,0 = jnz 0: if reg[a] != 0, goto beginning     # repeat


# ((((a % 8) ^ 7) ^ 7) ^ (a // (2 ** ((a % 8) ^ 7)))) % 8
# ((a % 8) ^ (a // (2 ** ((a % 8) ^ 7)))) % 8
# ((a % 8) ^ (a >> ((a % 8) ^ 7))) % 8

# 000 => shift a right 7 => (000 ^ (a >> 7)) % 8
# 001 => shift a right 6 => (001 ^ (a >> 6)) % 8
# 010 => shift a right 5 => (010 ^ (a >> 5)) % 8
# 011 => shift a right 4 => (011 ^ (a >> 4)) % 8
# 100 => shift a right 3 => (100 ^ (a >> 3)) % 8
# 101 => shift a right 2 => (101 ^ (a >> 2)) % 8 -- one bit determined    => XX0
# 110 => shift a right 1 => (110 ^ (a >> 1)) % 8 -- two bits determined   => X01
# 111 => shift a right 0 => (111 ^ (a >> 0)) % 8 -- three bits determined => 000


#def part2(data):
#    target = data[3][:]
#    program = data[3][:]
#
#    #A = 1 # start at 1, but we've gone up to...
#    A = 3_389_000_000
#    best = 0
#    while True:
#        try:
#            out = run_program(A, 0, 0, program, True)
#            print(f'{out=}, {program=}')
#            break
#        except Impossible as i:
#            o = i.args[0]
#            best = max(best, len(o))
#            if len(o) > 6:
#                print(f'{A=} failed {best=} {i=}')
#            elif (A % 1_000_000) == 0:
#                print(f'{A=} failed {best=} {i=}')
#        A += 1
#
#    return A

def find_recursive(vals, i, program):
    if i == len(program):
        return True

    print('starting', i)
    assert len(vals) == i
    vals.append(0)
    for a in range(8):
        vals[i] = a
        A = 0
        for ai in vals:
            A = (A << 3) | ai
        out = run_program(A, 0, 0, program)
        print(vals, a, A, out, program, i)
        if out[:i+1] == program[:i+1]:
            print('recursing, matched', i+1)
            if find_recursive(vals, i + 1, program):
                return True

    print('returning False for', i)
    vals.pop()
    return False

def part2(data):
    '''This is just a WIP'''
    program = data[3][:]

    vals = []

    find_recursive(vals, 0, program)

    return vals


def mogrify(line):
    if 'Register' in line:
        parts = line.split()
        name = parts[1][0]
        value = int(parts[-1])
        return value

    if 'Program' in line:
        return list(map(int, line.split()[-1].split(',')))

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = [line.rstrip('\n') for line in f]

    data = list(filter(lambda x: x is not None, map(mogrify, lines)))

    print('part 1:', part1(data))
    print('part 2:', part2(data))

if __name__ == '__main__':
    main()
