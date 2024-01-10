#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/7
Day 7: Camel Cards
"""

from collections import Counter
from functools import reduce
from timeit import timeit


def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 6440?')
    
    print('\npart 1:')
    print(part_1(data))
    
    #print('\nexample 2:')
    #print(part_2(ex_data), '= _?')
    
    #print('\npart 2:')
    #print(part_2(data))

    #breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = [(line[:5], int(line[6:-1])) for line in f]
    return data

def part_1(data):
    '''Find the rank of every hand in your set. What are the total winnings?'''
    hand_score = {
        (1, 1, 1, 1, 1): 1,  # A2345 high card
        (1, 1, 1, 2):    2,  # AA234 one pair
        (1, 2, 2):       3,  # AAJJ3 two pair
        (1, 1, 3):       4,  # AAA23 three of a kind
        (2, 3):          5,  # AAAJJ full house
        (1, 4):          6,  # AAAA2 four of a kind
        (5,):            7,  # AAAAA five of a kind
    }
    card_val = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14,
    }
    #print(timeit('for h,c in data: [n for _,n in c.most_common()]', globals=locals()))  # 1.97 s
    #print(timeit('for h,c in data: sorted(c.values())', globals=locals()))              # 0.54 s
    for i, (hand, bid) in enumerate(data):
        c = Counter(hand)
        sig = tuple(sorted(c.values()))
        score = hand_score[sig]
        cards = tuple(card_val[c] for c in hand)
        data[i] = (hand, bid, c, sig, score, cards) 
    data.sort(key=lambda d: (d[4], d[5]))
    #print(*((h, s, c) for h, _, _, _, s, c in data), sep='\n')
    return reduce(winnings, enumerate(data), 0)

def winnings(acc, e_hand):
    i, hand = e_hand
    bid = hand[1]
    rank = i + 1
    return acc + (bid * rank)

def part_2(data):
    '''assignment'''


if __name__ == '__main__':
    import sys
    sys.exit(main())

