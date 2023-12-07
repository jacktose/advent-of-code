#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/1
Day 1: Trebuchet?!
"""

import re

def main():
    ex_data_1 = get_input('./example_1')
    ex_data_2 = get_input('./example_2')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data_1), '= 142?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data_2), '= 281?')
    
    print('\npart 2:')
    print(part_2(data))

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
    '''What is the sum of all of the calibration values?'''
    digitize = {
        #'0': 0, 'zero': 0,
        '1': 1, 'one': 1,
        '2': 2, 'two': 2,
        '3': 3, 'three': 3,
        '4': 4, 'four': 4,
        '5': 5, 'five': 5,
        '6': 6, 'six': 6,
        '7': 7, 'seven': 7,
        '8': 8, 'eight': 8,
        '9': 9, 'nine': 9,
    }
    digitize_rev = {
        #'0': 0, 'orez': 0,
        '1': 1, 'eno': 1,
        '2': 2, 'owt': 2,
        '3': 3, 'eerht': 3,
        '4': 4, 'ruof': 4,
        '5': 5, 'evif': 5,
        '6': 6, 'xis': 6,
        '7': 7, 'neves': 7,
        '8': 8, 'thgie': 8,
        '9': 9, 'enin': 9,
    }
    sum = 0
    for line in data:
        digit_1 = re.search(r'\d|one|two|three|four|five|six|seven|eight|nine', line).group(0)
        digit_2 = re.search(r'\d|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin', line[::-1]).group(0)
        sum += (10 * digitize[digit_1]) + (1 * digitize_rev[digit_2])
    return sum


if __name__ == '__main__':
    import sys
    sys.exit(main())

