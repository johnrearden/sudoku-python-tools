import random
import time
from collections import defaultdict

from tools.classes import Puzzle
from tools.utils import recalculate_notes, choose_n_unknowns
from tools.uniqueness_test import is_unique
from solving_strategies.brute_force import brute_force


def create_sudoku_puzzle(filled_cells_count, valid_puzzle_dict):
    """
    A completed puzzle is created, and then cells removed one by one (but not
    reducing the number of unknowns to more than one digit below 1). If at any
    point the puzzle not longer has a unique solution, it is abandoned.
    """

    puzzle = Puzzle()
    brute_force(puzzle)

    indices_to_remove = choose_n_unknowns(puzzle, 81 - filled_cells_count)
    random.shuffle(indices_to_remove)

    # Main digit removal loop
    for idx, cell in enumerate(indices_to_remove):
        known_count = 81 - idx
        current_string = puzzle.to_short_string()
        puzzle.cells[cell] = 0
        clone = puzzle.clone()
        clone = recalculate_notes(clone)
        unique = is_unique(clone)
        if not unique:
            if known_count < 29:
                print(f'But valid puzzle with {known_count} knowns found')
                valid_puzzle_dict[known_count].append(current_string)
            return False
    valid_puzzle_dict[filled_cells_count].append(puzzle.to_short_string())
    return True


if __name__ == '__main__':
    counter = 1
    start_time = time.perf_counter()
    valid_puzzle_dict = defaultdict(list)
    while True:
        known_count = 20
        duration = time.perf_counter() - start_time
        if duration > 3600:
            print('An hour has passed ..... halting')
            break
        print(f'Attempt {counter}, time: {duration:0.2f}\r', end='')
        solved = create_sudoku_puzzle(known_count, valid_puzzle_dict)
        counter += 1
        if solved:
            duration = time.perf_counter() - start_time
            print(
                f'created a {known_count} knowns puzzle on attempt '
                f'{counter} in {duration:0.2f}s'
            )
            break

    for key in valid_puzzle_dict:
        print(f'{key} knowns')
        for puzzle in valid_puzzle_dict[key]:
            print(f'\t{puzzle}')
