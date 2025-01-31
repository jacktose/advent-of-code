#!/usr/env/python3

"""
Helpers for fancy printing.
Should probably just use Rich, Blessings, ncurses, notcurses, ....
"""

from typing import NamedTuple

class _fg(NamedTuple):
    BLACK =   '\x1b[30m'
    RED =     '\x1b[31m'
    GREEN =   '\x1b[32m'
    YELLOW =  '\x1b[33m'
    BLUE =    '\x1b[34m'
    MAGENTA = '\x1b[35m'
    CYAN =    '\x1b[36m'
    WHITE =   '\x1b[37m'

class _bg(NamedTuple):
    BLACK =   '\x1b[40m'
    RED =     '\x1b[41m'
    GREEN =   '\x1b[42m'
    YELLOW =  '\x1b[43m'
    BLUE =    '\x1b[44m'
    MAGENTA = '\x1b[45m'
    CYAN =    '\x1b[46m'
    WHITE =   '\x1b[47m'

class style(NamedTuple):
    RESET =         '\x1b[0m'
    BOLD =          '\x1b[1m'
    FAINT =         '\x1b[2m'
    ITALIC =        '\x1b[3m'
    UNDERLINED =    '\x1b[4m'
    INVERSE =       '\x1b[7m'
    STRIKETHROUGH = '\x1b[9m'
    FG = _fg
    BG = _bg

class control(NamedTuple):
    SHOW_CURSOR = '\x1b[?25h'
    HIDE_CURSOR = '\x1b[?25l'
    ERASE_CURSOR_TO_END = '\x1b[0J'
    ERASE_CURSOR_TO_START = '\x1b[1J'
    ERASE_SCREEN = '\x1b[2J'


if __name__ == '__main__':
    print(f'{style.BOLD}{style.FG.BLUE}Hello {style.RESET}{style.BG.MAGENTA}{style.UNDERLINED}world!{style.RESET}')