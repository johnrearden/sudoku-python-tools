from transformations.digit_substitution import substitute_digits
from transformations.rotation import rotate_puzzle_string
from transformations.shuffle_stacks import shuffle_stacks
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
from solving_strategies.swordfish import swordfish_rows, swordfish_cols
from solving_strategies.brute_force import brute_force
from tools.uniqueness_test import is_unique
from tools.classes import Puzzle
from tools.solve_with_strategies import solve_with_strategies

import csv


def main():
    with open('data/finished/all_finished/finished.csv', 'r') as file:

        simple_strats = [
            one_per_nonet,
            hidden_single,
            naked_pairs,
            naked_triples,
            naked_quads,
            hidden_pairs,
            hidden_triples,
        ]
        advanced_strats = [
            x_wing_cols,
            x_wing_rows,
            locked_candidates_claiming,
            locked_candidates_pointing,
            swordfish_cols,
            swordfish_rows
        ]
        all_strats = [*simple_strats, *advanced_strats]

        csv_reader = csv.reader(file)
        for puzzle_row in csv_reader:
            # if puzzle_row[2] == 'simple':
            #     continue
            print(puzzle_row)
            new_string = shuffle_stacks(puzzle_row[1])

            # Confirm puzzle still has unique solution
            puzzle = Puzzle()
            puzzle.build_from_string(new_string)
            unique = is_unique(puzzle)
            print(f'Puzzle is still unique: {unique}')

            # Confirm puzzle can still be solved with same strategy groups
            strategies = []
            if puzzle_row[2] == 'simple':
                strategies = simple_strats
                result = solve_with_strategies(new_string, strategies)
                print(f'result for simple strat puzzle: {result}')
            else:
                strategies = simple_strats
                result = solve_with_strategies(new_string, strategies)
                print(f'result for adv puzzle with simple strats: {result}')
                result = solve_with_strategies(new_string, all_strats)
                print(f'result for adv puzzle with all strats: {result}')
                result = solve_with_strategies(puzzle_row[1], all_strats)
                print(f'result for original with all_strats: {result}')

            print()
            print()
            
            
def main2():
    puzzle_string = '---3-42---1-9----------179-4----9---3--1--5----52---8---9-8---3-------162--------'
    puzzle = Puzzle()
    puzzle.build_from_string(puzzle_string)
    print(puzzle)
    
    str = shuffle_stacks(puzzle_string)
    puzzle = Puzzle()
    puzzle.build_from_string(str)
    print(puzzle)


if __name__ == '__main__':
    main2()
