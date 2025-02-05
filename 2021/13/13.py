#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/13
Day 13: Transparent Origami
"""

import sys
from collections import namedtuple

def main():
    ex_dots, ex_folds = get_input('./example.txt')
    dots, folds = get_input('./input.txt')
    
    print('example 1:')
    print(part_1(ex_dots, ex_folds, debug=False), '= 17?')
    
    print('\npart 1:')
    print(part_1(dots, folds), 'dots')
    
    print('\nexample 2:')
    print(part_2(ex_dots, ex_folds, debug=True))
    
    print('\npart 2:')
    print(part_2(dots, folds))
    #breakpoint()

def get_input(file='./input.txt'):
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
    new_dots = fold(dots, folds[0:1])
    if debug: print(dot_string(new_dots))
    return len(new_dots)

def part_2(dots, folds, debug=False):
    '''What code (eight capital letters) do you use to activate the infrared thermal imaging camera system?'''
    new_dots = fold(dots, folds, debug)
    return dot_string(new_dots)

Dot = namedtuple('Dot', ['x', 'y'])
Fold = namedtuple('Fold', ['axis', 'dim'])

def fold(dots, folds, debug=False):
    for fold in folds:
        if debug: print(dot_string(dots, fold), end='\n\n')
        new_dots = set()
        for dot in dots:
            if getattr(dot, fold.axis) < fold.dim:  # not beyond the fold
                new_dots.add(dot)
            else:  # beyond the fold
                new_val = 2*fold.dim - getattr(dot, fold.axis)
                new_dots.add(dot._replace(**{fold.axis: new_val}))
        dots = new_dots
    return tuple(new_dots)

def dot_string(dots, fold=None):
    DOT = '⬤'
    NO_DOT = '·'
    len_x, len_y = (max(i)+1 for i in zip(*dots))
    # initialize 2D list of no dots:
    grid = [[NO_DOT] * len_x for row in range(len_y)]
    # overwrite with fold characters:
    if fold and fold.axis == 'x':
        for row in grid:
            row[fold.dim] = '|'
    elif fold and fold.axis == 'y':
        grid[fold.dim] = ['-'] * (len_x)
    # overwrite with dots:
    for dot in dots:
        grid[dot.y][dot.x] = DOT
    return '\n'.join(''.join(row) for row in grid)


if __name__ == '__main__':
    sys.exit(main())

