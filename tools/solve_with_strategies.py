from tools.classes import Puzzle
from tools.utils import puzzle_complete
from tools.constants import SolverResult

from collections import defaultdict


def solve_with_strategies(puzzle_string, solvers, verbose=False):
    puzzle = Puzzle()
    puzzle.build_from_string(puzzle_string)
    solver_usage = defaultdict(int)

    while True:
        at_least_one_success = False
        for _, solver in enumerate(solvers):
            puzzle_changed = solver(puzzle)
            if verbose:
                print(f'{solver.__name__} : {puzzle_changed}')
            if puzzle_changed != SolverResult.NO_CHANGE:
                at_least_one_success = True
                solver_usage[solver.__name__] += 1
                if verbose:
                    print(puzzle.remaining_cells())
                    print('------')
                break
        if not at_least_one_success:
            if verbose:
                print('no solution with these solvers')
            break
        if puzzle_complete(puzzle):
            if verbose:
                print('Puzzle is solved')
                print(solver_usage)
            return puzzle.to_short_string()
            break