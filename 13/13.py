#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/13
Day 13: Transparent Origami
"""

import sys
from collections import namedtuple

def main():
    ex_dots, ex_folds = get_input('./example')
    dots, folds = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_dots, ex_folds, debug=True), '= 17?')
    
    print('\npart 1:')
    print(part_1(dots, folds), 'dots')
    
    #print('\nexample 2:')
    #print(part_2(ex_dots, ex_folds))
    
    #print('\npart 2:')
    #print(part_2(dots, folds))
    #breakpoint()

def get_input(file='./input'):
    dots = []
    folds = []
    with open(file, 'r') as f:
        for line in f:
            if line == '\n': break
            dots.append(Dot(*(int(n) for n in line.rstrip().split(','))))
        for line in f:
            folds.append(Fold(axis=line[11:12], dim=int(line[13:-1])))
    return tuple(dots), tuple(folds)

def part_1(dots, folds, debug=False):
    '''How many dots are visible after completing just the first fold instruction on your transparent paper?'''
    fold = folds[0]
    new_dots = set()
    for dot in dots:
        if getattr(dot, fold.axis) < fold.dim:  # not beyond the fold
            new_dots.add(dot)
        else:  # beyond the fold
            if fold.axis == 'x':  # figure out how to do this once for either
                new_x = 2*fold.dim - dot.x
                new_dots.add(Dot(new_x, dot.y))
            elif fold.axis == 'y':
                new_y = 2*fold.dim - dot.y
                new_dots.add(Dot(dot.x, new_y))
    if debug: print(new_dots)
    return len(new_dots)

def part_2(data):
    '''assignment'''

Dot = namedtuple('Dot', ['x', 'y'])
Fold = namedtuple('Fold', ['axis', 'dim'])

if __name__ == '__main__':
    sys.exit(main())

