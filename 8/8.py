#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/8
Day 8: Seven Segment Search
"""

import sys

def main():
    ex1_data = get_input('./example1')
    ex2_data = get_input('./example2')
    data = get_input()

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
    #breakpoint()

def get_input(file='./input'):
    '''transform input file of lines like
    gbcefa eac acfbg ae dcabfg begcdaf ecgba fgaedc beaf gcbde | cbgfa gedcb fgecab fbagdc
    to list of tuples like
    (('gbcefa', 'eac', 'acfbg', 'ae', 'dcabfg', 'begcdaf', 'ecgba', 'fgaedc', 'beaf', 'gcbde'), ('cbgfa', 'gedcb', 'fgecab', 'fbagdc'))
    '''
    with open(file, 'r') as f:
        data = [(tuple(d[:58].split()), tuple(d[61:].split())) for d in f.readlines()]
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
        output_digits = (str(decode(pattern, key)) for pattern in output_scrambled)
        output_number = int(''.join(str(d) for d in output_digits))
        if debug:
            print(f'{" ".join(output_scrambled)} ->\t{output_number}')
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
    patterns = (set(p) for p in signals)
    digits = {}
    digits[235] = []
    digits[690] = []
    
    for p in patterns:
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
    segs['adg'] = set.intersection(*digits[235])
    segs['abfg'] = set.intersection(*digits[690])
    segs['a'] = segs['acf'] - segs['cf']
    segs['b'] = segs['abfg'] - segs['acf'] - segs['adg']
    segs['c'] = segs['cf'] - segs['abfg']
    segs['d'] = segs['adg'] - segs['abfg']
    segs['e'] = segs['abcdefg'] - segs['abfg'] - segs['bcdf']
    segs['f'] = segs['cf'] - segs['c']
    segs['g'] = segs['adg'] - segs['a'] - segs['d']
    
    segtrans = {segs[s].pop(): s for s in 'abcdefg'}
    return str.maketrans(segtrans)

_digit = {
    'abcefg':   0,
    'cf':       1,
    'acdeg':    2,
    'acdfg':    3,
    'bcdf':     4,
    'abdfg':    5,
    'abdefg':   6,
    'acf':      7,
    'abcdefg':  8,
    'abcdfg':   9,
}
def decode(segments_scrambled, key):
    '''e.g. 'gbcefa' -> 'abdefg' -> 6'''
    segments = ''.join(sorted(segments_scrambled.translate(key)))
    return _digit[segments]


if __name__ == '__main__':
    sys.exit(main())

