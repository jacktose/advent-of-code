#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/3
Day 3: Mull It Over
"""

import re

def main():
    ex_data_1 = get_input('./example1')
    ex_data_2 = get_input('./example2')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data_1), '= 161?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data_2), '= 48?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = f.read()
    return data

def part_1(data):
    '''Scan the corrupted memory for uncorrupted mul instructions.
    What do you get if you add up all of the results of the multiplications?'''
    mul_re = r'(?s)mul\((\d{1,3}),(\d{1,3})\)'
    muls = re.findall(mul_re, data)
    return sum(int(a) * int(b) for (a,b) in muls)

def part_2(data):
    '''Handle the new instructions; what do you get if you
    add up all of the results of just the enabled multiplications?'''
    mul_re = r"(?s)mul\((\d{1,3}),(\d{1,3})\)|(do(?:n't)?\(\))"
    allresult = re.findall(mul_re, data)
    enable: bool = True
    total = 0
    for result in allresult:
        match result[2]:
            case 'do()':
                enable = True
            case "don't()":
                enable = False
            case '':
                total += int(result[0]) * int(result[1]) * enable
    return total


if __name__ == '__main__':
    import sys
    sys.exit(main())
