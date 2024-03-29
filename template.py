#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/_

"""

def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= _?')
    
    #print('\npart 1:')
    #print(part_1(data))
    
    #print('\nexample 2:')
    #print(part_2(ex_data), '= _?')
    
    #print('\npart 2:')
    #print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def part_1(data):
    '''assignment'''

def part_2(data):
    '''assignment'''


if __name__ == '__main__':
    import sys
    sys.exit(main())

