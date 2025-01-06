#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/9
Day 9: Disk Fragmenter
"""

from collections.abc import Sequence
from itertools import accumulate
from typing import Any


def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 1928?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 2858?')
    print(part_2b(ex_data), '= 2858?')
    
    print('\npart 2:')
    print(part_2(data))
    print(part_2b(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = f.read().strip()
    return data

def part_1(data: Sequence[str|int]) -> int:
    '''Compact the amphipod's hard drive using the process he requested.
    What is the resulting filesystem checksum?'''
    disk_layout = expand_disk(data)
    disk_layout = compact_frag(disk_layout)
    return checksum(disk_layout)

def expand_disk(disk_map: Sequence[int|str]) -> list[str]:
    '''12345 -> 0..111....22222'''
    layout = []
    for i, n in enumerate(disk_map):
        layout.extend(['.' if i & 1 else str(-(i//-2))] * int(n))
    return layout

def compact_frag(disk_layout: Sequence[int|str]) -> list[str]:
    disk: list = list(disk_layout)
    first_free: int = 0
    while True:
        while (block := disk.pop()) == '.':
            pass
        try:
            first_free = disk.index('.', first_free)
        except ValueError:
            disk.append(block)
            break
        disk[first_free] = block
    return disk

# TODO?: Objectify Disk with this approach for methods:
def compact_frag_b(disk_layout: Sequence[int|str]) -> list[str]:
    disk = list(disk_layout)
    #first_free: int = 0
    last_block: int = len(disk) - 1
    for i, c in enumerate(disk):
        if c == '.':
            if (last_block := rfind_last_block(disk, start=last_block)) <= i:
                break
            else:
                disk[i] = str(disk[last_block])
                disk[last_block] = '.'
    return disk

def rfind_last_block(seq: Sequence, start: int = -1, free: Any = '.') -> int:
    if start == -1:
        start = len(seq) - 1
    for i in range(start, -1, -1):
        if seq[i] != free:
            return i
    else:
        raise ValueError(f'{free} not found')

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
            #print(f'move F#{file_no} (idx{i_file}, len{file_length}) to '
            #      f'{addrs[i_free]} (idx{i_free}), cs{cs_file(addrs[i_free], file_length, file_no)}')
            checksum += cs_file(addrs[i_free], file_length, file_no)
            disk[i_free] = free_length - file_length
            addrs[i_free] += file_length
            break
        else:
            checksum += cs_file(addrs[i_file], file_length, file_no)
    return checksum

def cs_file(i_start: int, file_length: int, file_no: int) -> int:
    '''Checksum for a single file'''
    return file_no * (file_length * (file_length + 2*i_start - 1)) // 2
    # Sum of arithmetic series (indices) * file_no. Equivalent to:
    #return sum(i * file_no for i in range(i_start, i_start+file_length))  # Math betterly?

def part_2b(data: Sequence[str|int]) -> int:
    # Contstruct separate lists of files and frees:
    files = [(file_addr := 0,            int(data[0]))]
    for i in range(2, len(data), 2):
        a, b, c = (int(n) for n in data[i-2:i+1])
        file_addr += (a + b)
        files.append((file_addr, c))
    frees = [(free_addr := int(data[0]), int(data[1]))]
    for i in range(3, len(data), 2):
        a, b, c = (int(n) for n in data[i-2:i+1])
        free_addr += (a + b)
        frees.append((free_addr, c))

    # Find frees for each file and calculate checksum as we go
    # (don't bother modifying files):
    checksum = 0
    for file_no in range(len(files)-1, -1, -1):
        file_addr, file_length = files[file_no]
        for free_i in range(file_no):
            free_addr, free_length = frees[free_i]
            if free_length < file_length:
                continue
            checksum += cs_file(free_addr, file_length, file_no)
            frees[free_i] = (free_addr+file_length, free_length-file_length)
            break
        else:
            checksum += cs_file(file_addr, file_length, file_no)
    return checksum

#def part_2c(data) -> int:
#    disk_layout = compact_nofrag(data)
#    disk_layout = expand_disk(disk_layout)
#    return checksum(disk_layout)
#
#def compact_nofrag(data: Sequence[int|str]) -> list[int]:
#    disk = [int(n) for n in data]
#    # Process each file from the end:
#    for i_file in range(len(data) & ~1, -1, -2):
#        file_length = disk[i_file]
#        file_no = i_file // 2
#        # Check each free from the start:
#        for i_free in range(1, len(data), 2):
#            free_length = disk[i_free]
#            if file_length > free_length:
#                continue
#            # If it fits:
#            # Replace free-file-free with free of total size:
#            disk[i_file-1:i_file+2] = [sum(disk[i_file-1:i_file+2])]
#            # Replace (left-er) free with 0_free-file-remaining_free:
#            disk[i_free:i_free+1] = [0, file_length, free_length-file_length]
#            # OOPS! Didn't maintain file number from original position.
#            break
#        else:
#            # Leave file where it is
#            pass
#    return disk


if __name__ == '__main__':
    import sys
    sys.exit(main())
