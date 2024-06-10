import random
import sys
import time
from collections import defaultdict

from tools.classes import Puzzle
from tools.constants import SolverResult
from tools.utils import (
    puzzle_complete, recalculate_notes, choose_n_unknowns,
    get_puzzle_cells_as_string
)
from tools.uniqueness_test import is_unique

from solving_strategies.one_per_nonet import one_per_nonet
from solving_strategies.hidden_single import hidden_single
from solving_strategies.naked_pairs import naked_pairs
from solving_strategies.naked_triples import naked_triples
from solving_strategies.hidden_pairs import hidden_pairs
from solving_strategies.hidden_triples import hidden_triples
from solving_strategies.brute_force import brute_force
from solving_strategies.naked_quads import naked_quads
from solving_strategies.x_wing import x_wing_rows, x_wing_cols
from solving_strategies.locked_candidates import locked_candidates_pointing
from solving_strategies.locked_candidates import locked_candidates_claiming


def create_sudoku_puzzle(filled_cells_count):
    """
    A completed puzzle is created, and the cells are removed all in one go.
    The puzzle is then tested for a unique solution once only.
    """
    puzzle = Puzzle()
    brute_force(puzzle)
    # print(puzzle)

    indices_to_remove = choose_n_unknowns(
        puzzle, 
        81 - filled_cells_count,
        require_one_of_each_digit=True
        )

    # Main digit removal loop
    for cell_index in indices_to_remove:
        puzzle.cells[cell_index] = 0

    clone = puzzle.clone()
    clone = recalculate_notes(clone)
    unique = is_unique(clone)
    if unique:
        print('Puzzle has a unique solution')
        print(get_puzzle_cells_as_string(puzzle))
        return True
    else:
        # print('Puzzle not unique, unfortunately')
        return False


if __name__ == '__main__':
    counter = 1
    start_time = time.perf_counter()
    while True:
        known_count = 29
        duration = time.perf_counter() - start_time
        print(f'Attempt {counter}, time: {duration:0.2f}\r', end='')
        solved = create_sudoku_puzzle(known_count)
        counter += 1
        if solved:
            duration = time.perf_counter() - start_time
            print(
                f'created a {known_count} knowns puzzle on attempt '
                f'{counter} in {duration:0.2f}s'
            )
            break
    