#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/14
Day 14: Extended Polymerization
"""

import sys
from collections import Counter
from itertools import pairwise
from functools import reduce

def main():
    ex_template, ex_insertions = get_input('./example')
    template, insertions = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_template, ex_insertions, steps=10, debug=True))
    
    print('\npart 1:')
    print(part_1(template, insertions, steps=10, debug=False))
    
    #print('\nexample 2:')
    #print(part_2(ex_data))
    
    #print('\npart 2:')
    #print(part_2(data))
    #breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        template = f.readline().rstrip()
        _ = f.readline()
        insertions = dict((line.rstrip().split(' -> ')) for line in f)
    return template, insertions

def part_1(template, insertions, steps=10, debug=False):
    '''What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?'''
    if debug: print('Template:    ', template)
    for step in range(steps):
        polymer = reduce(lambda a,b: a+insertions[a[-1]+b]+b, template)
        if debug: print(f'After step {step+1}:', polymer)
        template = polymer
    c = Counter(polymer)
    if debug: print(f'{c.most_common()[0] =}\n{c.most_common()[-1] =}')
    return c.most_common()[0][1] - c.most_common()[-1][1]

def part_2(data):
    '''assignment'''


if __name__ == '__main__':
    sys.exit(main())

