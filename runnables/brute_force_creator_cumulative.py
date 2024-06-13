from tools.classes import Puzzle
from solving_strategies.brute_force import brute_force
from tools.utils import populate_digit_map, get_puzzle_cells_as_string
from tools.uniqueness_test import is_unique

import time
import random


def brute_force_create_puzzle(num_knowns):
    """
    The idea behind this approach is that the puzzle would not be thrown 
    away if no solution could be found at a certain depth of removals.
    Instead, each possible digit left to remove will be tried in turn, until
    we are out of digits or we find a solution
    """
    
    counter = 1
    start_time = time.perf_counter()
    while True:
        duration = time.perf_counter() - start_time
        print(f'Attempt {counter}, time: {duration:0.2f}\r', end='')
        solved = create_sudoku_puzzle(num_knowns)
        counter += 1
        if solved:
            duration = time.perf_counter() - start_time
            print(
                f'created a {num_knowns} knowns puzzle on attempt '
                f'{counter} in {duration:0.2f}s'
            )
            break


def create_sudoku_puzzle(num_knowns):
    puzzle = Puzzle()
    brute_force(puzzle, randomize_digit_order=True)  # A complete puzzle.
    num_to_remove = 81 - num_knowns
    digit_map = populate_digit_map(puzzle)

    # Main digit removal loop
    while num_to_remove > 0:
        #print(f'len(map) : {len(digit_map)}')
        if not digit_map:
            #print('Cant select another digit to remove')
            return False
        rand_key = random.choice(list(digit_map.keys()))
        cell_index = digit_map[rand_key].pop()
        cached_value = puzzle.cells[cell_index]
        puzzle.cells[cell_index] = 0
        
        # Check length of arrays in digit_map
        keys_to_remove = []
        for key in digit_map:
            if len(digit_map) == 9:
                if len(digit_map[key]) == 0:
                    keys_to_remove.append(key)
            elif len(digit_map) < 9:
                if len(digit_map[key]) == 1:
                    keys_to_remove.append(key)
        for key in keys_to_remove:
            del digit_map[key]
        #print(f'attempting to remove value from {cell_index}')

        # Check for uniqueness
        clone_for_uniqueness = puzzle.clone()
        unique = is_unique(clone_for_uniqueness, verbose=False)
        if not unique:
            # print('Puzzle does not have a unique solution')
            puzzle.cells[cell_index] = cached_value
        
    # We've removed all the digits, and the puzzle can be solved and has
    # a unique solution
    pzl_str = get_puzzle_cells_as_string(puzzle)
    print(pzl_str)
    return True


if __name__ == '__main__':
    brute_force_create_puzzle(50)