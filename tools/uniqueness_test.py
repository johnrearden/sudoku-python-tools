from tools.utils import (
    check_cell_validity, check_puzzle_validity, recalculate_notes,
    recalculate_cell_notes, get_puzzle_cells_as_string
)
import time
import random


def is_unique(
        puzzle,
        verbose=False):
    """
    Method creates a stack of unknown cells, and moves a pointer through the
    stack. If it encounters a cell with no possible digits remaining, it
    backtracks. If there are possible digits remaining, it chooses one and 
    """

    ALL_POSSIBLES = [n for n in range(1, 10)]

    unknown_cells = []
    possibles = []

    for index, cell in enumerate(puzzle.cells):
        if cell == 0:
            unknown_cells.append(index)
            possibles.append(ALL_POSSIBLES)

    pointer = 0
    counter = 0
    backtracking = False
    puzzle = recalculate_notes(puzzle)
    start_time = time.perf_counter()
    
    solution_set = set()

    while True:
        counter += 1
        if counter % 10000 == 0:
            if verbose:
                print(puzzle)
            t = time.perf_counter() - start_time
            known = puzzle.get_known_cells_count()
            print(f'counter {counter} time {t:0.1f} known: {known}\r', end="")
        if counter > 100000000:
            raise Exception('More than 10 million iterations ... no result')

        # First halting condition - cell at bottom of stack has no solution
        if len(possibles[0]) == 0 and pointer == 0:
            if len(solution_set) == 0:
                print('puzzle has no solution! counter=', counter)
                return False
            else:
                print('puzzle has no other solution - solution is unique!')
                return True

        cell_index = unknown_cells[pointer]

        # Before trying a new value in this cell, if we are not backtracking, 
        # recalculate the notes to eliminate impossible choices
        if not backtracking:
            possibles[pointer] = recalculate_cell_notes(cell_index, puzzle)
            random.shuffle(possibles[pointer])

        # If no possibles remain for this cell, we're at a dead end. Reset the
        # cell to 0, and backtrack by decrementing the pointer.
        if len(possibles[pointer]) == 0:
            puzzle.cells[cell_index] = 0
            pointer -= 1
            backtracking = True
            continue

        # At least one possible remains for this cell - try it, removing it
        # from the possibles list.
        candidate = possibles[pointer].pop()
        puzzle.cells[cell_index] = candidate

        # If the grid is still legal, increment the pointer and refill the
        # possibles array. Otherwise, remove the added candidate and loop again
        if check_cell_validity(cell_index, puzzle):
            pointer += 1
            backtracking = False

            # Last unknown cell has a value. We have at least one solution.
            
            if pointer >= len(unknown_cells):
                solution_str = get_puzzle_cells_as_string(puzzle)
                solution_set.add(solution_str)
                if len(solution_set) > 1:
                    print('More than one solution found! Puzzle is not unique')
                    return False
                else:
                    # Backtrack to try other solutions
                    puzzle.cells[cell_index] = 0
                    pointer -= 1
                    backtracking = True
        else:
            puzzle.cells[cell_index] = 0
