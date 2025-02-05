#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/14
Day 14: Extended Polymerization
"""

import sys
from collections import Counter
from itertools import pairwise

def main():
    ex_template, ex_insertions = get_input('./example.txt')
    template, insertions = get_input('./input.txt')
    
    print('example 1:')
    print(polymerize(ex_template, ex_insertions, steps=10, debug=True), '= 1588?')
    
    print('\npart 1:')
    print(polymerize(template, insertions, steps=10, debug=False), '= 2408?')
    
    print('\nexample 2:')
    print(polymerize(ex_template, ex_insertions, steps=40, debug=True), '= 2188189693529?')
    
    print('\npart 2:')
    print(polymerize(template, insertions, steps=40, debug=False))
    # 0.003910795999981929 s/loop

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        template = f.readline().rstrip()
        f.readline()
        insertions = {line[0:2]: line[6] for line in f}
    return template, insertions

def polymerize(template, insertions, steps=1, debug=False):
    '''What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?'''
    pairs = Counter(template[i:i+2] for i in range(len(template)-1))
    for step in range(steps):
        for pair, n in pairs.copy().items():
            pairs[pair] -= n
            pairs[pair[0] + insertions[pair]] += n
            pairs[insertions[pair] + pair[1]] += n

    chars = Counter(template[0])
    for pair, n in pairs.items():
        chars.update({pair[1]: n})

    if debug:
        print('polymer length:', chars.total())
        print(dict(chars.most_common()))
    return chars.most_common()[0][1] - chars.most_common()[-1][1]


if __name__ == '__main__':
    sys.exit(main())

