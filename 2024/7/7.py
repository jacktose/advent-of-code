#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/7
Day 7: Bridge Repair
"""

from operator import add, mul
from typing import Callable, Sequence


def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 3749?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 11387?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = [(int(target), tuple(int(num) for num in nums.split()))
                for (target, nums) in (line.split(':', maxsplit=1) for line in f)]  # Too much?
    return data

def part_1(data: list[tuple[int, tuple[int, ...]]]) -> int:
    '''Determine which equations could possibly be true.
    What is their total calibration result?'''
    return sum(target for target, nums in data if mathable(target, nums))

def part_2(data: list[tuple[int, tuple[int, ...]]]) -> int:
    '''Using your new knowledge of elephant hiding spots, determine which equations could possibly be true.
    What is their total calibration result?'''
    return sum(target for target, nums in data if mathable(target, nums, ops=(add, mul, cat)))

def mathable(target: int, nums: tuple[int, ...], ops: Sequence[Callable] = (add, mul)) -> bool:
    '''Recurse through values trying operations to find a valid equation'''
    if nums == (target,):
        return True
    if len(nums) < 2:
        return False
    if nums[0] > target:
        return False
    return any(
        mathable(target, (op(*nums[0:2]),) + nums[2:], ops=ops)
        for op in ops
    )

def cat(a: int|str, b: int|str) -> int:
    '''Concatenate two numbers'''
    return int(str(a) + str(b))


if __name__ == '__main__':
    import sys
    sys.exit(main())
