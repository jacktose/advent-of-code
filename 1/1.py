#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/1
Various attempts because I kept being slightly off. Turns out comparison works
as intended with strings, except across length boundaries. ><
"""

import sys

def main():
    with open('./input', 'r') as f:
        depths = [int(x) for x in f.readlines()]  # not explicitly casting to int *almost* works :[
    #print(len(depths))
    #print(depths)
    
    print(count_increases_1(depths))
    #print(count_increases_2(depths))
    print(count_increases_3(depths))
    
def count_increases_1(depths):
    '''First attempt'''
    increases = 0
    for i in range(len(depths)-1):
        if depths[i] < depths[i+1]:
            increases += 1
    return increases

def count_increases_2(depths):
    '''Very explicit, aped example when _1 gave wrong answer'''
    increases = 0
    prev_d = None
    for d in depths:
        if prev_d is None:
            print(f'{d} (N/A - no previous measurement)')
        elif d > prev_d:
            increases += 1
            print(f'{d} (increased) {increases}')
        elif d < prev_d:
            print(f'{d} (decreased)')
        elif d == prev_d:
            print(f'{d} (same)')
        prev_d = d
    return increases

def count_increases_3(depths):
    '''The fun one I wanted to write, but actually cribbed from reddit'''
    return sum((b>a) for (a,b) in zip(depths, depths[1:]))

if __name__ == '__main__':
    sys.exit(main())

