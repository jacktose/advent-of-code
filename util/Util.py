#!/usr/bin/python3

"""
Miscellaneous functions that I frequently want.
"""

from collections.abc import Sequence
import sys
from typing import Any


def find(sequence: Sequence, value: Any, start: int = 0, stop: int = sys.maxsize, /) -> int:
    '''Return index of value in sequence.
    Like str.find(), return -1 if value is not found.'''
    try:
        return sequence.index(value, start, stop)
    except ValueError:
        return -1
