#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/11
Day 11: Plutonian Pebbles
"""

from collections.abc import Iterable
from functools import lru_cache


def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1:')
    print(part_1(ex_data), '= 55312?')
    
    print('\npart 1:')
    print(part_1(data))
    print(num_after_blinking.cache_info())
    print(blink.cache_info())
    
    print('\nexample 2:')
    print(part_2(ex_data), '= ?')
    
    print('\npart 2:')
    print(part_2(data))
    print(num_after_blinking.cache_info())
    print(blink.cache_info())

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        data = tuple(int(n) for n in f.read().split())
    return data

def part_1(data: Iterable[int]) -> int:
    '''How many stones will you have after blinking 25 times?'''
    return sum(num_after_blinking(stone, 25) for stone in data)

def part_2(data: Iterable[int]) -> int:
    '''How many stones would you have after blinking a total of 75 times?'''
    return sum(num_after_blinking(stone, 75) for stone in data)

@lru_cache(maxsize=2**17)
def num_after_blinking(stone: int, n: int = 25) -> int:
    #TODO: Maybe there's a smarter way to cache this? Save the result after multiple steps?
    if n == 0:
        return 1
    next_step = blink(stone)
    return sum(num_after_blinking(s, n-1) for s in next_step)

@lru_cache(maxsize=2**12)
def blink(stone: int) -> tuple[int] | tuple[int, int]:
    if stone == 0:
        return (1,)
    elif len(stone_str := str(stone)) % 2 == 0:
        midpoint = len(stone_str)//2
        return (int(stone_str[:midpoint]), int(stone_str[midpoint:]))
    else:
        return (stone * 2024,)


if __name__ == '__main__':
    import sys
    sys.exit(main())

