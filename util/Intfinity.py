#!/usr/env/python3

"""
Infinity that's an instance of int, not float.
"""

import math

class _IntFinity(int):
    def __lt__(self, other) -> bool:
        return False
    def __le__(self, other) -> bool:
        return self.__eq__(other)
    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) or other == math.inf
    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
    def __gt__(self, other) -> bool:
        return self.__ne__(other)
    def __ge__(self, other) -> bool:
        return True

intfinity = _IntFinity()

if __name__ == '__main__':
    mi = math.inf
    x = intfinity
    y = intfinity
    z = _IntFinity()

    print(f'{type(intfinity) = }')
    print(f'{isinstance(intfinity, int) = }')
    print(f'{type(x) = }')
    print(f'{isinstance(x, int) = }')
    print()

    print(f'{(mi<mi) = }')
    print(f'{(x<mi) = }')
    print(f'{(x<x) = }')
    print(f'{(x<y) = }')
    print(f'{(x<z) = }')
    print()

    print(f'{(mi<=mi) = }')
    print(f'{(x<=mi) = }')
    print(f'{(x<=x) = }')
    print(f'{(x<=y) = }')
    print(f'{(x<=z) = }')
    print()

    print(f'{(mi==mi) = }')
    print(f'{(x==mi) = }')
    print(f'{(x==x) = }')
    print(f'{(x==y) = }')
    print(f'{(x==z) = }')
    print()

    print(f'{(mi!=mi) = }')
    print(f'{(x!=mi) = }')
    print(f'{(x!=x) = }')
    print(f'{(x!=y) = }')
    print(f'{(x!=z) = }')
    print()

    print(f'{(mi>mi) = }')
    print(f'{(x>mi) = }')
    print(f'{(x>x) = }')
    print(f'{(x>y) = }')
    print(f'{(x>z) = }')
    print()

    print(f'{(mi>=mi) = }')
    print(f'{(x>=mi) = }')
    print(f'{(x>=x) = }')
    print(f'{(x>=y) = }')
    print(f'{(x>=z) = }')
    print()