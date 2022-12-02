#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/7
Day 7: The Treachery of Whales
"""

import sys
from math import floor, ceil
from statistics import median, mean

def main():
    example()
    data = get_input()
    print('\npart 1:')
    print(part_1(data))
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = [int(n) for n in f.read().split(',')]
    return data

def example():
    crabs = [16,1,2,0,4,2,7,1,2,14]
    print('example 1:')
    print(f'{crabs = }')
    print(f'{median(crabs) = }')
    print(part_1(crabs))
    print('example 2:')
    print(f'{mean(crabs) = }')
    print(part_2(crabs))

def part_1(crabs):
    '''constant fuel burn'''
    target = int(median(crabs))
    cost = sum(abs(crab - target) for crab in crabs)
    return target, cost

def part_2(crabs):
    '''triangular number fuel burn'''
    target_float = mean(crabs)
    targets = [ floor(target_float), ceil(target_float) ]
    t_and_c = [ (target, sum(triangular(abs(crab - target)) for crab in crabs)) for target in targets ]
    return min(t_and_c, key=lambda x: x[1])

def triangular(n):
    '''nth triangular number'''
    #if n < 0 or n != int(n):
    #    raise ValueError(f'invalid n: {n}; sequence number must be natural number')
    return n * (n+1) // 2

if __name__ == '__main__':
    sys.exit(main())

