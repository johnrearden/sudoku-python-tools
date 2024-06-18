from solving_strategies.one_per_nonet import one_per_nonet
from solving_strategies.hidden_single import hidden_single
from solving_strategies.naked_pairs import naked_pairs
from solving_strategies.naked_triples import naked_triples
from solving_strategies.hidden_pairs import hidden_pairs
from solving_strategies.hidden_triples import hidden_triples
from solving_strategies.naked_quads import naked_quads
from solving_strategies.x_wing import x_wing_rows
from solving_strategies.x_wing import x_wing_cols
from solving_strategies.locked_candidates import locked_candidates_pointing
from solving_strategies.locked_candidates import locked_candidates_claiming
from solving_strategies.swordfish import swordfish_rows

from tools.classes import Puzzle
from tools.utils import puzzle_complete
from tools.constants import SolverResult

from collections import defaultdict
import csv


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


def main():
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
        swordfish_rows,
    ]

    with open('data/mined_puzzles/below_28_knowns.csv', 'r') as infile:
        puzzle_dict = defaultdict(list)
        reader = csv.reader(infile, delimiter=',')
        for row in reader:
            known_count = row[0]
            puzzle_string = row[1]
            puzzle_dict[known_count].append(puzzle_string)

    solvables = defaultdict(list)
    non_solvables = defaultdict(list)
    solvables_count = 0
    non_solvables_count = 0

    # for k, v in puzzle_dict.items():
    k = '23'
    v = puzzle_dict[k]
    for idx, puzzle_string in enumerate(v):
        result = solve_with_strategies(puzzle_string, solvers)
        # print('-------------------------')
        # print(f'Puzzle ({k}) {puzzle_string}')
        if result:
            solvables[k].append(puzzle_string)
            solvables_count += 1
            # print(f'solution: {result} : {idx}/{len(v)}')
        else:
            non_solvables[k].append(puzzle_string)
            non_solvables_count += 1
            # print(f'No solution found : {idx}/{len(v)}')

        print(f'{solvables_count} solvable, {non_solvables_count} not.\r', end='')
    print(f'{solvables_count} solvable, {non_solvables_count} not.')


if __name__ == '__main__':
    main()
