#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/4
Bingo with a squid!
"""

import sys
from pprint import pprint

def main():
    data = get_input()
    print('part 1:')
    print(part_1(data))
    print('\npart 2:')
    print(part_2(data))

def get_input(file='./input'):
    with open(file, 'r') as f:
        #data = f.read().splitlines()
        data = f.read().split('\n\n')
    return data

def part_1(data):
    '''Find the first winning board's score'''
    draws = data[0].split(',')
    boards = [Board(b) for b in data[1:]]
    #print(f'parsed {len(boards)} boards')
    for number in draws:
        print(number, end=' ')
        for board in boards:
            board.mark(number)
            if board.bingo:
                print('\nWINNER!')
                pprint(board.board)
                pprint(board.marks)
                #print(f'{board.score() = }')
                return board.score()
    else:
        return False

def part_2(data):
    '''Find the last winning board's score'''
    draws = data.pop(0).split(',')
    boards = [Board(b) for b in data]
    #print(f'parsed {len(boards)} boards')
    bingo_boards = []
    for number in draws:
        print(number, end=' ')
        for board in boards:
            if board.bingo:
                continue
            board.mark(number)
            if board.bingo:
                bingo_boards.append(board)
    print('\nLast winner:')
    pprint(bingo_boards[-1].board)
    pprint(bingo_boards[-1].marks)
    #print(f'final score: {bingo_boards[-1].score() = }')
    return bingo_boards[-1].score()


class Board:
    '''One bingo board, with state'''
    def __init__(self, boardstring):
        self.board = tuple(row.split() for row in tuple(boardstring.strip().split('\n')))
        self.marks = [[False]*len(row) for row in self.board]
        self.last_draw = None
        self.bingo = False

    def mark(self, number):
        '''Mark board space if&where number is found'''
        number = str(number)
        self.last_draw = number
        for row_idx, row_nos in enumerate(self.board):
            try:
                col_idx = row_nos.index(number)
                break
            except ValueError:
                continue
        else:
            return False
        #print(f'found {number} at row {row_idx}, col {col_idx}')
        self.marks[row_idx][col_idx] = True
        self.bingo = self._bingo()
        return True

    def _bingo(self):
        '''Does this board have a bingo?'''
        for row_idx, row in enumerate(self.marks):
            if False not in row:
                #print(f'BINGO! in row {row_idx}')
                return True
        for col_idx in range(len(self.marks[0])):
            if False not in [row[col_idx] for row in self.marks]:
                #print(f'BINGO! in col {col_idx}')
                return True
        return False

    def score(self):
        '''Calculate board "score" as defined by challenge'''
        #Start by finding the sum of all unmarked numbers on that board
        score = 0
        for row_idx, row in enumerate(self.board):
            for col_idx, number in enumerate(row):
                if self.marks[row_idx][col_idx] is False:
                    score += int(number)
        #Then, multiply that sum by the number that was just called when the board won to get the final score
        score *= int(self.last_draw)
        return score


if __name__ == '__main__':
    sys.exit(main())

