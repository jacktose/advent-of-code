#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/4

"""

import sys

def main():
    data = get_input()
    print('part 1:')
    print(part_1(data))
    #print('\npart 2:')
    #print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def part_1(data):


if __name__ == '__main__':
    sys.exit(main())

