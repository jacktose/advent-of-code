#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/_

"""

import sys

def main():
    data = get_input()
    print(part_1(data))
    #print(part_2(data))
    breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def part_1(data):
    '''assignment'''
    print('part 1:')

def part_2(data):
    '''assignment'''
    print('part 2:')


if __name__ == '__main__':
    sys.exit(main())

