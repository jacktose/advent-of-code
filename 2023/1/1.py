#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/1

"""

import re

def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 142?')
    
    print('\npart 1:')
    print(part_1(data))
    
    #print('\nexample 2:')
    #print(part_2(ex_data), '= _?')
    
    #print('\npart 2:')
    #print(part_2(data))

    #breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def part_1(data):
    '''What is the sum of all of the calibration values?'''
    sum = 0
    for line in data:
        digits = re.findall(r'\d', line)
        sum += int(digits[0] + digits[-1])
    return sum

def part_2(data):
    '''assignment'''


if __name__ == '__main__':
    import sys
    sys.exit(main())

