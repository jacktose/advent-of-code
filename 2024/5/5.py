#!/usr/bin/env python3

"""
https://adventofcode.com/2024/day/5
Day 5: Print Queue
"""

from collections import defaultdict

def main():
    ex_data = get_input('./example.txt')
    data = get_input('./input.txt')
    
    print('example 1:')
    print(part_1(ex_data), '= 143?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 123?')
    
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input.txt'):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    i_break = data.index('')
    d1 = [tuple(int(n) for n in line.split('|')) for line in data[:i_break]]
    d2 = [tuple(int(n) for n in line.split(',')) for line in data[i_break+1:]]
    
    # turn d1 (rules) into dict
    d1.sort()  # sorts on first member by default
    rules = defaultdict(list)
    for k, v in d1:
        rules[k].append(v)
    for k in rules:
        rules[k].sort()

    return rules, d2

def part_1(data):
    '''What do you get if you add up the middle page number
    from those correctly-ordered updates?'''
    rules, updates = data
    return sum(middle_val(update) for update in updates if is_ordered(update, rules))

def part_2(data):
    '''Find the updates which are not in the correct order.
    What do you get if you add up the middle page numbers
    after correctly ordering just those updates?'''
    rules, updates = data
    return sum(middle_val(order(update, rules)) for update in updates if not is_ordered(update, rules))

def is_ordered(pages, rules):
    '''Are the pages in order, acccording to the rules?'''
    for i, page in enumerate(pages):
        for successor in rules[page]:
            # Instead of KeyError, defaultdict(list) gives empty list,
            # which works here by effectively skipping the next loop:
            if successor in pages[:i]:
                return False
    else:
        return True

def order(pages, rules):
    '''Place all pages in order according to rules'''
    fixed = []
    for page in pages:
        successors = rules[page]
        # Put each page as late as possible without breaking a rule:
        fixed.insert(first_of_any(fixed, successors), page)
    return fixed

def first_of_any(seq, targets):
    '''Return index of first item that is in targets.
    If no target found, return length of sequence.'''
    for i, x in enumerate(seq):
        if x in targets:
            return i
    else:
        #raise ValueError('No target found in sequence')
        return len(seq)

def middle_val(seq):
    return seq[len(seq)//2]


if __name__ == '__main__':
    import sys
    sys.exit(main())
