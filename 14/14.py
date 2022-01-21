#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/14
Day 14: Extended Polymerization
"""

import sys
from collections import Counter
from itertools import pairwise

def main():
    ex_template, ex_insertions = get_input('./example')
    template, insertions = get_input('./input')
    
    print('example 1:')
    print(polymerize(ex_template, ex_insertions, steps=10, debug=True), '= 1588?')
    
    print('\npart 1:')
    print(polymerize(template, insertions, steps=10, debug=False), '= 2408?')
    
    print('\nexample 2:')
    print(polymerize(ex_template, ex_insertions, steps=40, debug=True), '= 2188189693529?')
    
    print('\npart 2:')
    print(polymerize(template, insertions, steps=40, debug=False))
    #breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        template = f.readline().rstrip()
        _ = f.readline()
        #insertions = dict((line.rstrip().split(' -> ')) for line in f)
        insertions = {(line[0], line[1]): line[6] for line in f}
    return template, insertions

def polymerize(template, insertions, steps=1, debug=False):
    '''What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?'''
    pairs = Counter(pairwise(template))
    for step in range(steps):
        for pair, n in pairs.copy().items():
            pairs[pair] -= n
            pairs.update({(pair[0], insertions[pair]): n,
                          (insertions[pair], pair[1]): n,})

    chars = Counter(template[0])
    for pair, n in pairs.items():
        chars.update({pair[1]: n})

    if debug:
        print(chars)
        print('polymer length:', chars.total())
        print(f'{chars.most_common()[0] = }\n{chars.most_common()[-1] = }')
    return chars.most_common()[0][1] - chars.most_common()[-1][1]


if __name__ == '__main__':
    sys.exit(main())

