from tools.utils import (
    check_cell_validity, check_puzzle_validity, recalculate_notes,
    recalculate_cell_notes, get_puzzle_cells_as_string
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
    Method creates a stack of unknown cells, and moves a pointer through the
    stack. If it encounters a cell with no possible digits remaining, it
    backtracks. If there are possible digits remaining, it chooses one and 
    """

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
    puzzle = recalculate_notes(puzzle)
    start_time = time.perf_counter()

    while True:
        counter += 1
        if counter % 10000 == 0:
            #input()
            if verbose:
                print(puzzle)
                t = time.perf_counter() - start_time
                known = puzzle.get_known_cells_count()
                print(f'counter {counter} time {t:0.1f} known: {known}\r', end="")
        if counter > 100000000:
            raise Exception('More than 10 million iterations ... no result')
            break

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
        # print('cell:', cell_index, ' , possibles:', possibles[pointer])

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
                # print(get_puzzle_cells_as_string(puzzle))
                # os.system('clear')
                # print(puzzle)
                # print("puzzle solved!")
                #print("iterations", counter)
                # print(f'time taken {time.perf_counter() - start_time:0.3f} seconds')
                return puzzle

            #possibles[pointer] = recalculate_cell_notes(cell_index, puzzle)
        else:
            puzzle.cells[cell_index] = 0
            
    return None
