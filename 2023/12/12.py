#!/usr/bin/env python3

"""
https://adventofcode.com/2023/day/12
Day 12: Hot Springs
"""

from functools import cache
import re

def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 21?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 525152?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = [tuple(l.split()) for l in f]
    return data

def part_1(data):
    '''For each row, count all of the different arrangements of
    operational and broken springs that meet the given criteria.
    What is the sum of those counts?'''
    records = ((s[0],
                tuple(int(n) for n in s[1].split(','))
               ) for s in data)
    return sum(ways(syms, nums) for (syms, nums) in records)

def part_2(data):
    '''Unfold your condition records;
    what is the new sum of possible arrangement counts?'''
    records = ((unfold(s[0], '?'),
                tuple(int(n) for n in unfold(s[1], ',').split(','))
               ) for s in data)
    return sum(ways(syms, nums) for (syms, nums) in records)

def unfold(orig: str, sep: str = '', n: int = 5) -> str:
    return sep.join(orig for _ in range(n))

@cache
def ways(springs: str, nums: tuple[int, ...]) -> int:
    '''recurse'''

    if nums == ():  # No more '#' groups
        return 0 if '#' in springs else 1
    if len(springs) < sum(nums) + len(nums) - 1:
        # Can't fit remaining number groups into this string
        return 0
    
    # Start at first #/?
    first = re.search(r'[#?]', springs)
    if first is None:
        return 0
    i = first.start()
    end = i + nums[0]
    spring = first.group()

    if spring == '?':  # Imagine it both ways
        return ways('#'+springs[i+1:], nums) + ways(springs[i+1:], nums)

    # spring == '#'; Must consume expected number of #/?
    if '.' in springs[i:end]:  # Not enough #/? in a row
        return 0
    if end == len(springs):
        if len(nums) == 1:  # All done!
            return 1
        else:  # Leftover groups
            return 0
    if springs[end] == '#':  # Run too long
        return 0
    
    # Successfully consumed group, move on to the next
    return ways(springs[end+1:], nums[1:])


if __name__ == '__main__':
    import sys
    sys.exit(main())

