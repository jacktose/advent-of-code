#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/1
Day 1: Historian Hysteria
"""

from collections import Counter

def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 11?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 31?')
    
    print('\npart 2:')
    print(part_2(data))

    #breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = [sorted(t) for t in zip(*((int(n) for n in pair) for pair in (line.split() for line in f)))]
    return data

def part_1(data):
    '''What is the total distance between your lists?'''
    return sum(abs(a-b) for (a, b) in zip(*data))
    
def part_2(data):
    '''assignment'''
    r_counts = Counter(data[1])
    return sum(n * r_counts[n] for n in data[0])


if __name__ == '__main__':
    import sys
    sys.exit(main())

