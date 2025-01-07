#!/usr/bin/env python3

# https://adventofcode.com/2024/day/24 - "Crossed Wires"
# Author: Greg Hamerly

import sys

class Base:
    def __init__(self, name):
        self.cache = None
        self.name = name

    def value(self):
        if self.cache is None:
            self.cache = self._value()
        return self.cache

    def _value(self):
        return None

class Constant(Base):
    def __init__(self, name, val):
        super().__init__(name)
        self.val = val

    def _value(self):
        return self.val

    def __repr__(self):
        #return f'{self.name}: {self.val}'
        return f'{self.name}'

class Binary(Base):
    def __init__(self, name, a, b):
        super().__init__(name)
        self.a = a
        self.b = b

    def __repr__(self):
        return f'({self.a} {type(self).__name__} {self.b})'

class And(Binary):
    def _value(self):
        a = self.a.value()
        b = self.b.value()
        if a is False or b is False:
            return False
        if a is None or b is None:
            return None
        return a and b

class Or(Binary):
    def _value(self):
        a = self.a.value()
        b = self.b.value()
        if a is True or b is True:
            return True
        if a is None or b is None:
            return None
        return a or b

class Xor(Binary):
    def _value(self):
        a = self.a.value()
        b = self.b.value()
        if a is None or b is None:
            return None
        return a ^ b

def f(a, op, b, c):
    m = { 'AND': And, 'OR': Or, 'XOR': Xor }
    return m[op](c, a, b)

def part1(data):
    data = list(filter(None, data)) # get rid of the blank line

    constants = [l for l in data if l[0] == 'constant']
    operations = [l for l in data if l[0] == 'operation']

    graph = {name: Constant(name, int(val)) for _, name, val in constants}
    while len(graph) < len(data):
        for _, a, op, b, c in operations:
            if a in graph and b in graph and c not in graph:
                graph[c] = f(graph[a], op, graph[b], c)

    bits = []
    for name in sorted(graph, reverse=True):
        if name.startswith('z'):
            bits.append(graph[name].value())

            description = str(graph[name])
            
            # printing out the circuit helps think about part 2
            #print(name, len(description), description)

    bits = ''.join(map(str, bits))

    return int(bits, 2)

def part2(data):
    return 'this was not done'

def mogrify(line):
    if ':' in line:
        register, value = line.split(': ')
        return ('constant', register, value)

    if ' -> ' in line:
        parts = line.split()
        return ('operation',) + tuple(parts[:3]) + (parts[4],)

    return None

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
