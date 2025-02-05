#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/9
Day 9: Disk Fragmenter
"""

import sys
from collections.abc import Sequence
from itertools import accumulate


def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1:')
    print(part_1(ex_data), '= 1928?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 2858?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        data = f.read().strip()
    return data

def part_1(data: Sequence[str|int]) -> int:
    '''Compact the amphipod's hard drive using the process he requested.
    What is the resulting filesystem checksum?'''
    disk_layout = expand_disk(data)
    disk_layout = compact_frag(disk_layout)
    return checksum(disk_layout)

def expand_disk(disk_map: Sequence[int|str]) -> list[int|str]:
    '''12345 -> 0..111....22222
    (actually [0, '.', '.', 1, 1, 1, '.', ... ] to handle file nos > 9)'''
    layout = []
    for i, n in enumerate(disk_map):
        layout.extend(['.' if i & 1 else -(i//-2)] * int(n))
    return layout

def compact_frag(disk_layout: Sequence[int|str]) -> list[int|str]:
    '''Compact the disk, fragmenting files across free blocks'''
    disk = list(disk_layout)
    first_free: int = 0
    while (first_free := find(disk, '.', first_free)) != -1:
        while (block := disk.pop()) == '.':
            pass
        disk[first_free] = block
    return disk

def checksum(disk_layout: Sequence[int|str]) -> int:
    return sum(i*int(n) for i, n in enumerate(disk_layout) if n != '.')

def part_2(data: Sequence[str|int]) -> int:
    '''Compact the amphipod's hard drive using this new method instead.
    What is the resulting filesystem checksum?'''
    disk = [int(n) for n in data]
    addrs = list(accumulate(disk, initial=0))[:-1]
    checksum: int = 0
    # Process each file from the end:
    for i_file in range(len(data) & ~1, -1, -2):
        file_length = disk[i_file]
        file_no = i_file // 2
        # Try each free space from the start to the file location:
        for i_free in range(1, i_file, 2):
            free_length = disk[i_free]
            if file_length > free_length:
                continue
            # If a free spot is found, calculate the checksum and adjust the free space
            # as though the file has been inserted (no need to modify the file list):
            checksum += cs_file(addrs[i_free], file_length, file_no)
            disk[i_free] = free_length - file_length
            addrs[i_free] += file_length
            break
        else:
            checksum += cs_file(addrs[i_file], file_length, file_no)
    return checksum

def cs_file(i_start: int, file_length: int, file_no: int) -> int:
    '''Checksum for a single file'''
    # Sum of arithmetic series (indices) * file_no. Equivalent to:
    #return sum(i * file_no for i in range(i_start, i_start+file_length))
    return file_no * (file_length * (file_length + 2*i_start - 1)) // 2

def find[T](sequence: Sequence[T], value: T, start: int = 0, stop: int = sys.maxsize, /) -> int:
    '''Return the lowest index in the sequence where value is found within the slice s[start:end]. Return -1 if value is not found.
    (Like str.find() but for lists & other sequences.)'''
    try:
        return sequence.index(value, start, stop)
    except ValueError:
        return -1


if __name__ == '__main__':
    import sys
    sys.exit(main())
