#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/9
Day 9: Mirage Maintenance
"""

from itertools import pairwise
from typing import NamedTuple, Sequence

def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1:')
    print(part_1(ex_data), '= 114?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 2?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        data = [[int(n) for n in v.split()] for v in f.read().splitlines()]
    return data

def part_1(data: list[list[int]]) -> int:
    '''Analyze your OASIS report and extrapolate the next value for each history.
    What is the sum of these extrapolated values?'''
    return sum(extrapolate(value).next for value in data)

def part_2(data: list[list[int]]) -> int:
    '''Analyze your OASIS report again,
    this time extrapolating the previous value for each history.
    What is the sum of these extrapolated values?'''
    return sum(extrapolate(value).prev for value in data)

class Extraps(NamedTuple):
    prev: int
    next: int

def extrapolate(values: Sequence[int]) -> Extraps:
    prev: int = 0; coef: int = 1
    next: int = 0
    while any(x != 0 for x in values):
        prev += values[0] * coef; coef = -coef
        next += values[-1]
        values = [b - a for a, b in pairwise(values)]
        #print(values, prev, next)
    return Extraps(prev, next)


if __name__ == '__main__':
    import sys
    sys.exit(main())

