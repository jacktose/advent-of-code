#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/7
Day 7: Camel Cards
"""

from collections import Counter
from dataclasses import dataclass
from typing import ClassVar, Iterable

@dataclass
class Hand:
    cards: str
    bid: int
    joker: bool = False

    _hand_score: ClassVar[dict[tuple[int, ...], int]] = {
        (1, 1, 1, 1, 1): 1,  # A2345 high card
        (1, 1, 1, 2):    2,  # AA234 one pair
        (1, 2, 2):       3,  # AAJJ3 two pair
        (1, 1, 3):       4,  # AAA23 three of a kind
        (2, 3):          5,  # AAAJJ full house
        (1, 4):          6,  # AAAA2 four of a kind
        (5,):            7,  # AAAAA five of a kind
    }
    _card_val: ClassVar[dict[str, int]] = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14,
    }

    def __post_init__(self):
        self.effective_cards: str
        self.counter: Counter
        self._signature: tuple[int, ...]
        self._type_score: int
        self._card_values: tuple[int, int, int, int, int]
        self._sort_key: tuple[int, tuple[int, int, int, int, int]]

        if not self.joker or 'J' not in self.cards or self.cards == 'JJJJJ':
            self.effective_cards = self.cards
        else:
            # Demote 'J' from 11 to 1 (lowest)
            self._card_val['J'] = 1
            # Determine effective hand by adding jokers to modal (other) card
            common = Counter(self.cards).most_common(2)
            target = common[1][0] if common[0][0] == 'J' else common[0][0]
            self.effective_cards = self.cards.replace('J', target)

        self.counter = Counter(self.effective_cards)
        self._signature = tuple(sorted(self.counter.values()))
        self._type_score = self._hand_score[self._signature]
        self._card_values = tuple(self._card_val[c] for c in self.cards)  # type: ignore
        self._sort_key = (self._type_score, self._card_values)  # type: ignore

    def __lt__(self, other) -> bool:
        return self._sort_key < other._sort_key
    def __le__(self, other) -> bool:
        return self._sort_key <= other._sort_key
    def __gt__(self, other) -> bool:
        return self._sort_key > other._sort_key
    def __ge__(self, other) -> bool:
        return self._sort_key >= other._sort_key
    

def main():
    ex_data = get_input('./example')
    data = get_input('./input')
    
    print('example 1:')
    print(part_1(ex_data), '= 6440?')
    
    print('\npart 1:')
    print(part_1(data))
    
    print('\nexample 2:')
    print(part_2(ex_data), '= 5905?')
    
    print('\npart 2:')
    print(part_2(data))

    #breakpoint()

def get_input(file='./input'):
    with open(file, 'r') as f:
        data = [(line[:5], int(line[6:-1])) for line in f]
    return data

def part_1(data: Iterable[tuple[str, int]]) -> int:
    '''Find the rank of every hand in your set. What are the total winnings?'''
    hands = [Hand(*h) for h in data]
    return winnings(hands)

def part_2(data: Iterable[tuple[str, int]]) -> int:
    '''Using the new joker rule, find the rank of every hand in your set.
    What are the new total winnings?'''
    hands = [Hand(*h, joker=True) for h in data]
    return winnings(hands)

def winnings(hands: list[Hand]) -> int:
    hands.sort()
    return sum(hand.bid * (i+1) for i, hand in enumerate(hands))


if __name__ == '__main__':
    import sys
    sys.exit(main())

