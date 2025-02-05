#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/3
Day 3: Gear Ratios
"""

import re

def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 4361?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 467835?')
    
    print('\npart 2:')
    print(part_2(data))

    #breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    return data

def part_1(data):
    '''What is the sum of all of the part numbers in the engine schematic?'''
    total = 0
    for y, line in enumerate(data):
        #total += sum(int(match[0]) for match in re.finditer(r'\d+', line) if adjacent_to_symbol(data, y, *match.span()))
        for match in re.finditer(r'\d+', line):
            if adjacent_to_symbol(data, y, *match.span()):
                total += int(match[0])
    return total

def adjacent_to_symbol(data, y, start, end):
    '''Is the match object adjacent to a symbol?'''
    start = max(0, start-1)
    end = min(len(data[y]), end+1)
    
    neighbors = (data[y-1][start:end] if (y > 0) else '') \
        + (data[y][start:end]) \
        + (data[y+1][start:end] if (y < len(data) - 1) else '')
    
    return bool(re.search(r'[^0-9.]', neighbors))


def part_2(data):
    '''What is the sum of all of the gear ratios in your engine schematic?'''
    total = 0
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == '*':
                nums = adjacent_numbers(data, x, y)
                if len(nums) == 2:
                    total += nums[0] * nums[1]
    return total

def adjacent_numbers(data, x, y):
    matches  = [re.search(r'\d+$', data[y][0:x])]  #left
    matches += [re.search(r'^\d+', data[y][x+1:-1])]  #right
    matches += [match for match in re.finditer(r'\d+', data[y-1]) if adjacent_to_point(match, x)]  # above
    matches += [match for match in re.finditer(r'\d+', data[y+1]) if adjacent_to_point(match, x)]  # below
    return [int(match[0]) for match in matches if match is not None]
        
def adjacent_to_point(match, x):
    if match.end() < x:
        return False
    if match.start() > x+1:
        return False
    return True


if __name__ == '__main__':
    import sys
    sys.exit(main())
