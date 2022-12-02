#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/5
Day 5: Hydrothermal Venture
Much simplified version!
"""

import sys
import re
from collections import Counter

def main():
    with open('./input', 'r') as f:
        # turn 'a,b -> c,d' into (a, b, c, d)
        data = ( (int(n) for n in re.split(r'\D+', line)) for line in f.read().splitlines() )
    counts_1 = Counter()
    counts_2 = Counter()
    for line in data:
        x1, y1, x2, y2 = line
        if y1 == y2:  # horizontal
            points = tuple((x,y1) for x in ri_range(x1, x2))
            counts_1.update(points)
            counts_2.update(points)
        elif x1 == x2:  # vertical
            points = tuple((x1,y) for y in ri_range(y1, y2))
            counts_1.update(points)
            counts_2.update(points)
        else:  # diagonal
            # don't include in part 1
            counts_2.update(zip( ri_range(x1, x2), ri_range(y1, y2) ))  # can make better generator?
    print('part 1:', sum(n>1 for n in counts_1.values()))
    print('part 2:', sum(n>1 for n in counts_2.values()))
    #return sum(n>1 for n in counts_1.values()), sum(n>1 for n in counts_2.values())

def ri_range(start, stop):
    '''Reversible, Inclusive range
    R: Make the range run backwards if it wants to!
    I: Go the extra step
    '''
    if stop >= start:
        return range(start, stop+1, 1)
    else:
        return range(start, stop-1, -1)


if __name__ == '__main__':
    #from timeit import timeit
    #print(timeit(main, number=100))
    sys.exit(main())

