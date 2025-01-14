#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/_

"""

def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:', part_1(ex_data), '= _?')
    #print('\npart 1:', part_1(data))
    #print('\nexample 2:', part_2(ex_data), '= _?')
    #print('\npart 2:', part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        #data = f.read()
        data = f.read().splitlines()
        #data = tuple(tuple(line for line in chunk.splitlines()) for chunk in f.read.split('\n\n'))
        #data = tuple(tuple(int(n) for n in line.split()) for line in f)
    return data

def part_1(data):
    '''assignment'''

def part_2(data):
    '''assignment'''


if __name__ == '__main__':
    import sys
    sys.exit(main())
