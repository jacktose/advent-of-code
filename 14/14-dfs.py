#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/14
Day 14: Extended Polymerization
"""

import sys
from collections import Counter
from itertools import pairwise
from functools import cache
#import timeit

ex_insertions = {}
insertions = {}

def main():
    global ex_insertions
    global insertions
    ex_template, ex_insertions = get_input('./example')
    template, insertions = get_input('./input')
    
    print('example 1:')
    print(part_both(ex_template, steps=10, example=True, debug=True), '= 1588?')
    
    print('\npart 1:')
    print(part_both(template, steps=10, debug=False), '= 2408?')
    
    print('\nexample 2:')
    print(part_both(ex_template, steps=40, example=True, debug=True), '= 2188189693529?')
    
    print('\npart 2:')
    print(part_both(template, steps=40, debug=False))
    
    #print('\npart 2 timed:')
    #t = timeit.Timer(
    #    setup='template, insertions = get_input("./input")',
    #    stmt='part_both(template, steps=40)',
    #    globals=globals()
    #)
    #loops, secs = t.autorange()
    #print(loops, secs, secs/loops, 's/loop')
    # 0.000174637049989542 s/loop

def get_input(file='./input'):
    with open(file, 'r') as f:
        template = f.readline().rstrip()
        f.readline()
        insertions = {line[0:2]: line[6] for line in f}
    return template, insertions

def part_both(template, steps=1, example=False, debug=False):
    '''What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?'''
    pairs = polymerize(template, steps=steps, example=example, debug=debug)
    
    chars = Counter(template[0])
    for pair, n in pairs.items():
        chars.update({pair[1]: n})
    
    if debug:
        print('polymer length:', chars.total())
        print(dict(chars.most_common()))
    return chars.most_common()[0][1] - chars.most_common()[-1][1]
    
def part_both_f(template, steps=1, example=False, debug=False):
    '''Alternate arrangement using f() below'''
    chars = Counter(template)
    for a,b in zip(template, template[1:]):
        chars += f(a, b, steps, example)
    
    if debug:
        print('polymer length:', chars.total())
        print(dict(chars.most_common()))
    return chars.most_common()[0][1] - chars.most_common()[-1][1]

@cache
def polymerize(template, steps=1, example=False, debug=False):
    '''Recursion for depth-first search'''
    global ex_insertions, insertions  # can't pass in unhashable object
    ins = ex_insertions if example else insertions
    pairs = Counter(template[i:i+2] for i in range(len(template)-1))
    if steps == 0: return pairs
    for pair, n in pairs.copy().items():
        pairs[pair] -= n
        trio = pair[0] + ins[pair] + pair[1]
        pairs += polymerize(trio, steps=steps-1, example=example, debug=debug)
    return pairs

@cache
def f(a, b, steps, example=False):
    '''Cribbed from /u/4HbQ again
    https://www.reddit.com/r/adventofcode/comments/rfzq6f/2021_day_14_solutions/hohwxvd/
    '''
    global ex_insertions, insertions
    if steps == 0: return Counter('')
    i = ex_insertions[a+b] if example else insertions[a+b]
    c = Counter(i)
    c += f(a, i, steps-1)
    c += f(i, b, steps-1)
    return c


if __name__ == '__main__':
    sys.exit(main())

