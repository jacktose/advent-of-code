#!/usr/bin/env python3

"""
https://adventofcode.com/2022/day/5
Day 5: Supply Stacks
"""

from typing import NamedTuple
from copy import deepcopy
from itertools import takewhile

def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1:')
    print(part_1(*deepcopy(ex_data)), '= CMZ?')
    
    print('\npart 1:')
    print(part_1(*deepcopy(data)))
    
    print('\nexample 2:')
    print(part_2(*deepcopy(ex_data)), '= MCD?')
    
    print('\npart 2:')
    print(part_2(*deepcopy(data)))

    #breakpoint()

class Move(NamedTuple):
    count: int
    src: int
    dst: int

    @classmethod
    def from_string(cls, string):
        return cls(*(int(n) for n in string.split()[1::2]))

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        #layers = []
        #for line in f:
        #    if line == '\n': break
        #    crates = list(line[1::4])
        #    layers.append(crates)
        #layers = [list(line[1::4]) for line in iter(f.readline, '\n')]
        #layers = [list(line[1::4]) for line in takewhile(lambda line: line != '\n', f)]
        layers = [list(line[1::4]) for line in takewhile('\n'.__ne__, f)]
        stacks = {
            #int(stack[0]): [crate for crate in stack[1:] if crate != ' ']
            #int(stack[0]): list(takewhile(lambda crate: crate != ' ', stack[1:]))
            int(stack[0]): list(takewhile(' '.__ne__, stack[1:]))
            for stack in zip(*reversed(layers))
        }
        moves = [Move.from_string(line) for line in f]
    return stacks, moves

def part_1(stacks, moves):
    '''Move 1 crate at a time.
    After the rearrangement procedure completes, what crate ends up on top of each stack?'''
    for move in moves:
        for _ in range(move.count):
            stacks[move.dst].append(stacks[move.src].pop())
    return ''.join(stack[-1] for stack in stacks.values())

def part_2(stacks, moves):
    '''Move multiple crates at a time.
    After the rearrangement procedure completes, what crate ends up on top of each stack?'''
    for move in moves:
        stacks[move.dst].extend(stacks[move.src][-move.count:])
        del stacks[move.src][-move.count:]
    return ''.join(stack[-1] for stack in stacks.values())


if __name__ == '__main__':
    import sys
    sys.exit(main())

