#!/usr/bin/env python3

"""
https://adventofcode.com/2021/day/17
Day 17: Chronospatial Computer
"""

from collections.abc import Iterator, Sequence
from dataclasses import InitVar, dataclass, field
from typing import NamedTuple


def main():
    ex_data_1 = get_input('./example1.txt')
    ex_data_2 = get_input('./example2.txt')
    data = get_input('./input.txt')
    
    print('example 1:', part_1(ex_data_1), '= 4,6,3,5,6,3,5,2,1,0?', end='\n\n')
    print('part 1:',    part_1(data), end='\n\n')
    print('example 2:', a:=part_2(ex_data_2), '= 117440?', end='\n\n')
    print('part 2:',    a:=part_2(data), end='\n\n')  # 216_584_205_979_245 

def get_input(file='./input') -> tuple[dict[str, int], tuple[int, ...]]:
    with open(file, 'r') as f:
        registers_str, program_str = f.read().split('\n\n')
    registers: dict[str, int] = {line[9]: int(line[12:]) for line in registers_str.splitlines()}
    program: tuple[int, ...] = tuple(int(n) for n in program_str[9:].split(','))
    return registers, program

def part_1(data: tuple[dict[str, int], tuple[int, ...]]) -> str:
    '''initialize the registers to the given values, then run the program.
    What do you get if you use commas to join the values it output into a single string?'''
    registers, program = data

    #prog = Program(program)
    #return ','.join(map(str, prog.run(State(**registers))))

    compy = Computer(registers, program)
    return compy.format(compy.run())

def part_2(data: tuple[dict[str, int], tuple[int, ...]]) -> int:
    '''What is the lowest positive initial value for register A
    that causes the program to output a copy of itself?'''
    _, program = data
    prog = Program(program)
    return prog.find_quine()


class State(NamedTuple):
    '''State of VM, separated from Program'''
    A: int
    B: int
    C: int
    pointer: int = 0
    halted: bool = False

    def halt(self):
        return self._replace(halted=True)


class Program(tuple[int]):
    '''Program instruction tuple, plus methods to run it'''

    def __new__(cls, program: Sequence[int]):
        return super().__new__(cls, program)

    def run(self, state: State) -> Iterator[int]:
        while True:
            state, output = self.next_state_output(state)
            if state.halted or output is None:
                return
            yield output

    def run_a(self, A: int) -> tuple[int, ...]:
        '''run() but given only A, since the rest of state is irrelevant.'''
        return tuple(self.run(State(A=A, B=0, C=0)))
    
    def find_quine(self) -> int:
        '''
        Part 2: What is the lowest positive initial value for register A
                that causes the program to output a copy of itself?
        Really a convenience wrapper around the recursive generator find_a().
        '''
        return next(self.find_a(self))

    def find_a(self, target: tuple[int, ...]) -> Iterator[int]:
        '''Recursively find the lowest A that produces the program sequence.'''
        if target == ():    # base case
            yield 0         # start with 0 because ...
            return          # it's just a value to which we add more bits
        for a_bits_so_far in self.find_a(target[1:]):   # effectively backtrack when lowest ...
            for a_bits_new in range(8):                 # value can't produce later digits
                a_cand = (a_bits_so_far << 3) + a_bits_new
                if self.run_a(a_cand) == target:
                    yield a_cand

    def next_state_output(self, state: State) -> tuple[State, int|None]:
        '''Run program from given state until next output.'''
        output: int|None = None
        while output is None and not state.halted:
            state, output = self.next_state(state)
        return state, output

    def next_state(self, state: State) -> tuple[State, int|None]:
        '''Run program from given state for one operation.'''
        A, B, C, ip, _ = state
        try:
            op = self[ip + 1]
        except IndexError:
            return state.halt(), None
        combo = [0, 1, 2, 3, A, B, C][op]
        out: int|None = None
        match self[ip]:
            case 0: A >>= combo
            case 1: B  ^= op
            case 2: B   = combo & 7
            case 3: ip  = op - 2 if A else ip
            case 4: B  ^= C
            case 5: out = combo & 7
            case 6: B   = A >> combo
            case 7: C   = A >> combo
        return State(A, B, C, ip+2), out


@dataclass
class Computer:
    '''
    The VM described by the challenge. Implemented for Part 1.
    More complicated than Program, above, but left in for historical reasons.
    '''
    registers: InitVar[dict[str, int]]
    A: int = field(init=False)
    B: int = field(init=False)
    C: int = field(init=False)
    program: Sequence[int]

    def __post_init__(self, registers):
        for register, value in registers.items():
            self.__setattr__(register, value)
        self._registers_orig = registers.copy()
    
    def run(self, program: Sequence[int]|None = None) -> tuple[int, ...]:
        if program is None:
            program = self.program
        program = tuple(program)
        output: list[int] = []
        pointer: int = 0
        while pointer in range(len(program)):
            opcode = program[pointer]
            operand = program[pointer+1]
            match opcode:
                case 0: self.A = self.A // 2**self.combo(operand)
                case 1: self.B = self.B ^ operand
                case 2: self.B = self.combo(operand) % 8
                case 3:
                    if self.A:
                        pointer = operand - 2
                case 4: self.B = self.B ^ self.C
                case 5: output.append(self.combo(operand) % 8)
                case 6: self.B = self.A // 2**self.combo(operand)
                case 7: self.C = self.A // 2**self.combo(operand)
            pointer += 2
        return tuple(output)
    
    def combo(self, operand: int) -> int:
        match operand:
            case 0|1|2|3: return operand
            case 4: return self.A
            case 5: return self.B
            case 6: return self.C
            case _: raise ValueError(f'Invalid combo operand: {operand}')

    @classmethod
    def format(cls, output: Sequence[int]) -> str:
        '''"If a program outputs multiple values, they are separated by commas."'''
        return ','.join(str(n) for n in output)
    

def test():
    '''Minimal implementation of puzzle input program.'''
    output = {A: [] for A in range(136)}
    for A, thisout in output.items():
        while A != 0:
            B  = (A  & 7) ^ 3
            B ^= (A >> B) ^ 5
            thisout.append(B&7)
            A >>= 3
    #pprint(output)
    for A, out in output.items():
        print(f"{A}: {','.join(map(str, out))}")


if __name__ == '__main__':
    import sys
    sys.exit(main())
