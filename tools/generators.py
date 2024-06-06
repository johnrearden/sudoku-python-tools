from tools.utils import recalculate_notes, check_cell_validity
from tools.classes import Puzzle

import sys
import random


def naive_builder():
    ALL_DIGITS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    puzzle = Puzzle()
    for cell_index in range(81):
        digits = ALL_DIGITS[:]
        random.shuffle(digits)
        while True:
            if not digits:
                print(f'No candidates remain for cell {cell_index}')
                sys.exit()
            candidate = digits.pop()
            puzzle.cells[cell_index] = candidate
            if check_cell_validity(cell_index, puzzle):
                print(f'Placing {candidate} in cell {cell_index}')
                print(puzzle)
                break
            else:
                print(f'Cant place {candidate} in {cell_index}')
                print(puzzle)
