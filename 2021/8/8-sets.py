#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/8
Day 8: Seven Segment Search
"""

import sys
from timeit import timeit

fset = frozenset

def main():
    ex1_data = get_input('./example1.txt')
    ex2_data = get_input('./example2.txt')
    data = get_input('./input.txt')

    print('example 1:')
    print(part_1(ex2_data))
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2.1:')
    print(part_2(ex1_data, debug=True))
    
    print('\nexample 2.2:')
    print(part_2(ex2_data, debug=True))
    
    print('\npart 2:')
    print(part_2(data))
    #print(timeit(lambda: part_2(data), number=10_000))
    #breakpoint()

def get_input(file='./input.txt'):
    '''transform input file of lines like
    gbcefa eac acfbg ae dcabfg begcdaf ecgba fgaedc beaf gcbde | cbgfa gedcb fgecab fbagdc
    to list of tuples like
    (('gbcefa', 'eac', 'acfbg', 'ae', 'dcabfg', 'begcdaf', 'ecgba', 'fgaedc', 'beaf', 'gcbde'), ('cbgfa', 'gedcb', 'fgecab', 'fbagdc'))
    '''
    with open(file, 'r') as f:
        data = [
            (
                fset( map(fset, d[:58].split())),
                tuple(map(fset, d[61:].split())),
            ) for d in f.readlines()
        ]
    return data

def part_1(data):
    '''In the output values, how many times do digits 1, 4, 7, or 8 appear?'''
    count = 0
    for _, d in data:
        for digit in d:
            if len(digit) in (2,3,4,7):
                count += 1
    # ↑ is faster than comprehensions ↓
    #return sum([len(digit) in (2,3,4,7) for digit in d[1]].count(True) for d in data)
    #return len(list(filter(lambda s: len(s) in (2,3,4,7), itertools.chain.from_iterable(d[1] for d in data))))
    return count

def part_2(data, debug=False):
    '''For each entry, determine all of the wire/segment
    connections and decode the four-digit output values.
    What do you get if you add up all of the output values?
    '''
    total = 0
    for signal, output_scrambled in data:
        key = key_from_sigs(signal)
        output_digits = (decode(pattern, key) for pattern in output_scrambled)
        output_number = int(''.join(str(d) for d in output_digits))
        if debug:
            print(f'{" ".join("".join(sorted(p)) for p in output_scrambled)} ->\t{output_number}')
        total += output_number
    return total

def key_from_sigs(signals):
    '''from signals like:
    ('gbcefa', 'eac', 'acfbg', 'ae', 'dcabfg', 'begcdaf', 'ecgba', 'fgaedc', 'beaf', 'gcbde')
    to true segments:
     aaaa 
    b    c
    b    c
     dddd 
    e    f
    e    f
     gggg 
    '''
    digits = {}
    digits[235] = []
    digits[690] = []
    
    for p in signals:
        match len(p):
            case 2:  # 1
                digits[1] = p
            case 3:  # 7
                digits[7] = p
            case 4:  # 4
                digits[4] = p
            case 5:  # 2, 3, or 5
                digits[235].append(p)
            case 6:  # 0, 6, or 9
                digits[690].append(p)
            case 7:  # 8
                digits[8] = p
    
    segs = {}
    segs['cf'] = digits[1]
    segs['acf'] = digits[7]
    segs['bcdf'] = digits[4]
    segs['abcdefg'] = digits[8]
    segs['adg'] = fset.intersection(*digits[235])
    segs['abfg'] = fset.intersection(*digits[690])
    segs['a'] = segs['acf'] - segs['cf']
    segs['b'] = segs['abfg'] - segs['acf'] - segs['adg']
    segs['c'] = segs['cf'] - segs['abfg']
    segs['d'] = segs['adg'] - segs['abfg']
    segs['e'] = segs['abcdefg'] - segs['abfg'] - segs['bcdf']
    segs['f'] = segs['cf'] - segs['c']
    segs['g'] = segs['adg'] - segs['a'] - segs['d']
    
    segtrans = {next(iter(segs[s])): s for s in 'abcdefg'}
    return segtrans

_digit = {
    fset('abcefg'):  0,
    fset('cf'):      1,
    fset('acdeg'):   2,
    fset('acdfg'):   3,
    fset('bcdf'):    4,
    fset('abdfg'):   5,
    fset('abdefg'):  6,
    fset('acf'):     7,
    fset('abcdefg'): 8,
    fset('abcdfg'):  9,
}
def decode(segments_scrambled, key):
    '''e.g. 'gbcefa' -> 'abdefg' -> 6'''
    segments = fset(key[s] for s in segments_scrambled)
    return _digit[segments]


if __name__ == '__main__':
    sys.exit(main())

