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
    print(part_1(ex_dots, ex_folds, debug=False), '= 17?')
    
    print('\npart 1:')
    print(part_1(dots, folds), 'dots')
    
    print('\nexample 2:')
    print(part_2(ex_dots, ex_folds, debug=True))
    
    print('\npart 2:')
    print(part_2(dots, folds, debug=True))
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
                if fold.axis == 'x':  # figure out how to do this once for either
                    new_x = 2*fold.dim - dot.x
                    new_dots.add(Dot(new_x, dot.y))
                elif fold.axis == 'y':
                    new_y = 2*fold.dim - dot.y
                    new_dots.add(Dot(dot.x, new_y))
        dots = new_dots
    return tuple(new_dots)

def dot_string(dots, fold=None):
    DOT = '⬤'
    NO_DOT = '·'
    FOLD = fold.axis.translate({ord("x"): "|", ord("y"): "-"}) if fold else None
    max_x, max_y = (max(i) for i in zip(*dots))
    out = ''
    for y in range(max_y+1):
        for x in range(max_x+1):
            if Dot(x, y) in dots:
                out += DOT
            elif fold and eval(fold.axis) == fold.dim:
                out += FOLD
            else:
                out += NO_DOT
        out += '\n'
    return out.rstrip()

if __name__ == '__main__':
    sys.exit(main())

