from solving_strategies.x_wing import x_wing_rows
from solving_strategies.brute_force import brute_force

from tools.classes import Puzzle
from tools.utils import recalculate_notes


def main():
    x_wing_string = (
        '''1-----569492-561-8-561-924-'''
        '''--964-8-1-64-1----218-356-4'''
        '''-4-5---169-5-614-2621-----5'''
    )
    puzzle = Puzzle()
    puzzle.build_from_string(x_wing_string)
    brute_force(puzzle)
    
    puzzle = Puzzle()
    puzzle.build_from_string(x_wing_string)
    puzzle = recalculate_notes(puzzle)
    x_wing_rows(puzzle)


if __name__ == '__main__':
    main()