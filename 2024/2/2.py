#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/2
Day 2: Red-Nosed Reports
"""

from itertools import pairwise

def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 2?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 4?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = [[int(n) for n in line.split()] for line in f]
    return data

def part_1(data):
    '''How many reports are safe?'''
    return sum(safe(report) for report in data)

def part_2(data):
    '''Update your analysis by handling situations where the Problem Dampener can
    remove a single level from unsafe reports. How many reports are now safe?'''
    return sum(safe(report, dampen=1) for report in data)

#def safe(report):
#    safe_step = range(1, 4) if report[1] - report[0] > 0 else range(-3, 0)
#    for a, b in pairwise(report):
#        if not b-a in safe_step:
#            return False
#    return True

def safe(report, dampen=0):
    safe_step = range(1, 4) if report[1] - report[0] > 0 else range(-3, 0)
    for i, (a, b) in enumerate(pairwise(report)):
        if not b-a in safe_step:
            if dampen < 1:
                return False
            else:
                return any(safe(edited, dampen-1) for edited in (
                    report[:i-1] + report[i:],
                    report[:i]   + report[i+1:],
                    report[:i+1] + report[i+2:],
                ))
    return True


if __name__ == '__main__':
    import sys
    sys.exit(main())
