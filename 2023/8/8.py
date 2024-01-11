#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/8
Day 8: Haunted Wasteland
"""

import itertools
import math
from typing import Callable

def main():
    ex_data_1_1 = get_input('./example1.1')
    ex_data_1_2 = get_input('./example1.2')
    ex_data_2 = get_input('./example2')
    data = get_input('./input')
    
    print('example 1.1:')
    print(part_1(ex_data_1_1), '= 2?')
    print('example 1.2:')
    print(part_1(ex_data_1_2), '= 6?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data_2), '= 6?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    steps = [{'L': 0, 'R': 1}[step] for step in data[0]]
    nodes = {d[0:3]: (d[7:10], d[12:15]) for d in data[2:]}
    return steps, nodes

def part_1(data: tuple[list[int], dict[str, tuple[str, str]]]) -> int:
    '''Starting at AAA, follow the left/right instructions.
    How many steps are required to reach ZZZ?'''
    steps, nodes = data
    return path_len(steps, nodes, start='AAA', endfun=lambda node: node == 'ZZZ')

def part_2(data: tuple[list[int], dict[str, tuple[str, str]]]) -> int:
    '''Simultaneously start on every node that ends with A.
    How many steps does it take before you're only on nodes that end with Z?'''
    steps, nodes = data
    starts = [node for node in nodes.keys() if node.endswith('A')]
    dists = [path_len(steps, nodes, start=s, endfun=lambda node: node.endswith('Z')) for s in starts]
    #print(dists)
    return math.lcm(*dists)

def path_len(steps: list[int],
             nodes: dict[str, tuple[str, str]],
             start: str = 'AAA',
             endfun: Callable[[str], bool] = lambda node: node == 'ZZZ'
            ) -> int:
    pos = start
    for dist, step in enumerate(itertools.cycle(steps), start=1):
        pos = nodes[pos][step]
        if endfun(pos):
            return dist

if __name__ == '__main__':
    import sys
    sys.exit(main())

