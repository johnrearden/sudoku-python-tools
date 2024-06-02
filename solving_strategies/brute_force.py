from tools.utils import check_cell_validity, check_puzzle_validity
import os
import time
import random


def brute_force(puzzle, random_swaps=0, randomize_digit_order=False):
    """
    Method creates a stack of unknown cells, and moves a pointer through the
    stack. If it encounters a cell with no possible digits remaining, it
    backtracks. If there are possible digits remaining, it chooses one and 
    """

    ALL_POSSIBLES = [n for n in range(1, 10)]
    if randomize_digit_order:
        random.shuffle(ALL_POSSIBLES)
        print(ALL_POSSIBLES)

    unknown_cells = []
    possibles = []

    for index, cell in enumerate(puzzle.cells):
        if cell == 0:
            unknown_cells.append(index)
            possibles.append(ALL_POSSIBLES[:])
            
    for _ in range(random_swaps):
        i = random.randint(0, len(unknown_cells) - 1)
        j = random.randint(0, len(unknown_cells) - 1)
        temp = unknown_cells[i]
        unknown_cells[i] = unknown_cells[j]
        unknown_cells[j] = temp

    pointer = 0
    counter = 0
    start_time = time.perf_counter()

    while True:
        counter += 1
        if counter % 100000 == 0:
            print(f'counter {counter}\r', end="")
        if counter > 10000000:
            raise Exception('More than 10 million iterations ... no result')
            break
        
        # os.system('clear')
        # print(puzzle)
        
        if pointer == 0 and counter > 2:
            print('Back at start of unknowns list')

        # First halting condition - cell at bottom of stack has no solution
        if len(possibles[0]) == 0 and pointer == 0:
            print('puzzle has no solution! counter=', counter)
            print(puzzle)
            print(possibles)
            break

        cell_index = unknown_cells[pointer]

        # If no possibles remain for this cell, we're at a dead end. Reset the
        # cell to 0, and backtrack by decrementing the pointer.
        if len(possibles[pointer]) == 0:
            puzzle.cells[cell_index] = 0
            pointer -= 1
            continue

        # At least one possible remains for this cell - try it, removing it
        # from the possibles list.
        candidate = possibles[pointer].pop()
        puzzle.cells[cell_index] = candidate

        # If the grid is still legal, increment the pointer and refill the
        # possibles array. Otherwise, remove the added candidate and loop again
        if check_cell_validity(cell_index, puzzle):
            pointer += 1

            # 2nd halting condition. Last unknown cell has a value.
            if pointer >= len(unknown_cells):
                os.system('clear')
                print(puzzle)
                print("puzzle solved!")
                print("iterations", counter)
                print(f'time taken {time.perf_counter() - start_time:0.3f} seconds')
                return puzzle.cells

            possibles[pointer] = ALL_POSSIBLES[:]
        else:
            # print("illegal candidate", candidate, "at cell", cell_index)
            puzzle.cells[cell_index] = 0
