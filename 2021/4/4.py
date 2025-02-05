#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/4
Bingo with a squid!
"""

import sys
import math

def main():
    data = get_input()
    print('part 1:')
    print('score:', part_1(data))
    print('\npart 2:')
    print('score:', part_2(data))

def get_input(file='./input.txt'):
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
                print(board)
                #print(f'{board.score = }')
                return board.score
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
    print(bingo_boards[-1])
    #print(f'final score: {bingo_boards[-1].score = }')
    return bingo_boards[-1].score


class Board:
    '''One bingo board, with state'''
    def __init__(self, boardstring, markstring=None, _last_draw=None):
        self.board = tuple(boardstring.strip().split())  # ignore linebreaks, assuming board is square
        # needs to handle markstring input to have a valid __repr__
        if markstring:
            self.marks = [m=='True' for m in markstring.strip().split()]
            if len(self.marks) != len(self.board):
                raise ValueError('markstring does not match boardstring')
        else:
            self.marks = [False] * len(self.board)
        self._dimension = int(math.sqrt(len(self.board)))
        if self._dimension ** 2 != len(self.board):
            raise ValueError('board is not square')
        self.last_draw = _last_draw  # used for score calculation
        #breakpoint()
    
    def __repr__(self):
        ''' e.g.
        Board('36 13 44 81 48 93 88 41 77 57 6 64 2 3 46 30 10 8 20 14 26 76 7 1 90', 'False False False False False True True True True True False False False False True True False False True True False True False False False', '57')
        '''
        boardstring = ' '.join(self.board)
        markstring = ' '.join(str(m) for m in self.marks)
        return f"Board('{boardstring}', '{markstring}', '{self.last_draw}')"
    
    def __str__(self):
        ''' e.g.
        36  13  44  81  48 
        93* 88* 41* 77* 57*
         6  64   2   3  46*
        30* 10   8  20* 14*
        26  76*  7   1  90 
        '''
        #board = '\n'.join(' '.join((number + ('*' if mark else ' ')).rjust(3) for (number, mark) in zip(self.board[row*self._dimension : (row+1)*self._dimension], self.marks[row*self._dimension : (row+1)*self._dimension])) for row in range(self._dimension))
        board = ''
        for (i, n, m) in zip(range(len(self.board)), self.board, self.marks):
            mark = '*' if m else ' '
            board += (n + mark).rjust(3)
            board += '\n' if ((i+1) % self._dimension == 0) else ' '
        return board.strip()
    
    def mark(self, number):
        '''Mark board space if&where number is found'''
        number = str(number)
        self.last_draw = number
        try:
            idx = self.board.index(number)
        except ValueError:
            return False
        self.marks[idx] = True
        return True
    
    @property
    def bingo(self):
        '''Does this board have a bingo?'''
        for row in range(self._dimension):
            if False not in self.marks[row*self._dimension : (row*self._dimension)+self._dimension]:
                #print(f'BINGO! in row {row}')
                return True
        for col in range(self._dimension):
            if False not in self.marks[col::self._dimension]:
                #print(f'BINGO! in col {col}')
                return True
        return False
    
    @property
    def score(self):
        '''Calculate board "score" as defined by challenge'''
        #Start by finding the sum of all unmarked numbers on that board
        score = sum(int(n) for (n,m) in zip(self.board, self.marks) if m == False)
        #Then, multiply that sum by the number that was just called when the board won to get the final score
        score *= int(self.last_draw)
        return score


if __name__ == '__main__':
    sys.exit(main())

