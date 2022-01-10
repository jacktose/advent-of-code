#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/8
Day 8: Seven Segment Search
"""

import sys
#import itertools

def main():
    print('example:')
    ex_data = get_input('./example')
    print(part_1(ex_data))
    print('\npart 1:')
    data = get_input()
    print(part_1(data))
    #print('\npart 2:')
    #print(part_2(data))
    #breakpoint()

def get_input(file='./input'):
    '''transform input file of lines like
    gbcefa eac acfbg ae dcabfg begcdaf ecgba fgaedc beaf gcbde | cbgfa gedcb fgecab fbagdc
    to list of tuples like
    (('gbcefa', 'eac', 'acfbg', 'ae', 'dcabfg', 'begcdaf', 'ecgba', 'fgaedc', 'beaf', 'gcbde'), ('cbgfa', 'gedcb', 'fgecab', 'fbagdc'))
    '''
    with open(file, 'r') as f:
        data = [(tuple(d[:58].split()), tuple(d[61:].split())) for d in f.readlines()]
    return data

def part_1(data):
    '''In the output values, how many times do digits 1, 4, 7, or 8 appear?'''
    count = 0
    for _, d in data:
        for digit in d:
            if len(digit) in (2,3,4,7):
                count += 1
    # ↑ is faster than comprehensions ↓
    #return sum([len(digit) in (2,3,4,7) for digit in d[1]].count(True) for d in data)
    #return len(list(filter(lambda s: len(s) in (2,3,4,7), itertools.chain.from_iterable(d[1] for d in data))))
    #breakpoint()
    return count


if __name__ == '__main__':
    sys.exit(main())

