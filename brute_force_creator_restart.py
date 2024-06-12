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
    A completed puzzle is created, and then cells removed one by one (but not
    reducing the number of more than one digit below 1). If at any point the
    puzzle not longer has a unique solution, it is abandoned.
    """
    
    puzzle = Puzzle()
    brute_force(puzzle)
    #print(puzzle)

    indices_to_remove = choose_n_unknowns(puzzle, 81 - filled_cells_count)

    # Main digit removal loop
    for idx, cell in enumerate(indices_to_remove):
        puzzle.cells[cell] = 0
        clone = puzzle.clone()
        clone = recalculate_notes(clone)
        solved = solve_with_strategies(clone)
        if not solved:
            # print(f'Puzzle with {idx + 1} cells removed could not be solved')
            # input('Press Enter')
            # print(puzzle)
            return False
    # print(puzzle)
    
    clone = puzzle.clone()
    clone = recalculate_notes(clone)
    brute_force_result = brute_force(clone)
    if not brute_force_result:
        print(f'brute force not successful - puzzle invalid {brute_force_result}')
        return False
    
    clone = puzzle.clone()
    unique = is_unique(clone)
    if unique:
        print('Puzzle has a unique solution')
        print(get_puzzle_cells_as_string(puzzle))
        return True
    else:
        print('Puzzle not unique, unfortunately')
        return False


def solve_with_strategies(puzzle):
    solvers = [
        one_per_nonet,
        hidden_single,
        naked_pairs,
        naked_triples,
        hidden_pairs,
        hidden_triples,
        naked_quads,
        x_wing_rows,
        x_wing_cols,
        locked_candidates_pointing,
        locked_candidates_claiming,
    ]
    solver_usage = defaultdict(int)
    notes_only_changed_count = 0
    
    while True:

        at_least_one_success = False
        puzzle_solved = False
        for _, solver in enumerate(solvers):
            puzzle_changed = solver(puzzle)
            if puzzle_changed != SolverResult.NO_CHANGE:
                # print(f'{solver.__name__} successful')
                at_least_one_success = True
                solver_usage[solver.__name__] += 1
                if puzzle_complete(puzzle):
                    puzzle_solved = True

            if puzzle_changed == SolverResult.NOTES_ONLY_CHANGED:
                if notes_only_changed_count > len(solvers):
                    # print('Although notes changed, no new success')
                    return puzzle_solved
                notes_only_changed_count += 1
                # print(f'{solver.__name__} no results')
        if not at_least_one_success:
            #print('------------------------------')
            #print('no solution with these solvers')
            break
        if puzzle_solved:
            #
            # print('Puzzle is solved!')
            #print(solver_usage)
            break
    return puzzle_solved


if __name__ == '__main__':
    counter = 1
    start_time = time.perf_counter()
    while True:
        known_count = 32
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
    