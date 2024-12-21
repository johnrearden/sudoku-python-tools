from tools.utils import (
    check_puzzle_validity,
    check_cell_validity,
    recalculate_notes,
    recalculate_cell_notes
)
import time
import random


def brute_force(
        puzzle,
        random_swaps=0,
        randomize_digit_order=False,
        reverse_grid=False,
        shuffle=False,
        verbose=False):
    """
    Solve a Sudoku puzzle using a brute force algorithm.

    This method attempts to solve a Sudoku puzzle by creating a stack of 
    unknown cells and moving a pointer through the stack. If it encounters 
    a cell with no possible digits remaining, it backtracks. If there are 
    possible digits remaining, it chooses one and continues.

    Parameters:
    puzzle (Puzzle): The Sudoku puzzle to be solved.
    random_swaps (int, optional): Number of random swaps to perform on the 
        unknown cells. Default is 0.
    randomize_digit_order (bool, optional): If True, randomize the order of 
        digits to try in each cell. Default is False.
    reverse_grid (bool, optional): If True, solve the puzzle starting from 
        the last cell. Default is False.
    shuffle (bool, optional): If True, shuffle the unknown cells before 
        solving. Default is False.
    verbose (bool, optional): If True, print detailed information during the 
        solving process. Default is False.

    Returns:
    The solved puzzle, or None if no solution is found.

    Raises:
    ValueError: If the puzzle is invalid or unsolvable.

    """

    # Perform basic validation on puzzle
    if not check_puzzle_validity(puzzle) or len(puzzle.cells) != 81:
        raise ValueError('Puzzle is not valid')
    
    # Check that only the digits 1 to 9 and the dash symbol occur in 
    # puzzle.cells
    for cell in puzzle.cells:
        if cell not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            raise ValueError('Puzzle contains invalid characters')

    ALL_POSSIBLES = [n for n in range(1, 10)]
    if randomize_digit_order:
        random.shuffle(ALL_POSSIBLES)
        # print(ALL_POSSIBLES)

    unknown_cells = []
    possibles = []

    for index, cell in enumerate(puzzle.cells):
        if cell == 0:
            unknown_cells.append(index)
            possibles.append(ALL_POSSIBLES)

    for _ in range(random_swaps):
        i = random.randint(0, len(unknown_cells) - 1)
        j = random.randint(0, len(unknown_cells) - 1)
        temp = unknown_cells[i]
        unknown_cells[i] = unknown_cells[j]
        unknown_cells[j] = temp

    if reverse_grid:
        unknown_cells.reverse()

    if shuffle:
        random.shuffle(unknown_cells)

    pointer = 0
    counter = 0
    backtracking = False

    # Before starting, recalculate the notes for all cells
    puzzle = recalculate_notes(puzzle)
    start_time = time.perf_counter()

    while True:
        counter += 1
        if counter % 10000 == 0:
            # input()
            if verbose:
                print(puzzle)
                t = time.perf_counter() - start_time
                known = puzzle.get_known_cells_count()
                print(
                    f'counter {counter} time {t:0.1f} known: {known}\r',
                    end="")
        if counter > 100000000:
            raise Exception('More than 10 million iterations ... no result')

        # First halting condition - cell at bottom of stack has no solution
        if len(possibles[0]) == 0 and pointer == 0:
            print('puzzle has no solution! ! counter=', counter)
            break

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

            # 2nd halting condition. Last unknown cell has a value.
            if pointer >= len(unknown_cells):
                return puzzle

        else:
            puzzle.cells[cell_index] = 0
            
    return None
