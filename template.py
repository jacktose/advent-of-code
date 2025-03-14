#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/_

"""

def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1:', part_1(ex_data), '= _?',    '\n')
    #print('part 1:',    part_1(data),               '\n')
    #print('example 2:', part_2(ex_data), '= _?',    '\n')
    #print('part 2:',    part_2(data),               '\n')

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        #data = f.read()
        data = f.read().splitlines()
        #data = tuple(tuple(line for line in chunk.splitlines()) for chunk in f.read().split('\n\n'))
        #data = tuple(tuple(int(n) for n in line.split()) for line in f)
    return data

def part_1(data):
    '''assignment'''

def part_2(data):
    '''assignment'''


if __name__ == '__main__':
    import sys
    sys.exit(main())
