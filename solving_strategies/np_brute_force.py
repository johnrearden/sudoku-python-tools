import time
import numpy as np


def np_brute_force(
        original_puzzle,
        randomize_digit_order=False,
        verbose=False):

    puzzle = original_puzzle.clone()
    puzzle.calculate_notes(remove_only=False)

    unknown_cells = [i for i in range(0, 81) if puzzle.cells[i] == 0]
    unknowns = np.array(unknown_cells)

    pointer = 0
    counter = 0
    backtracking = False
    start_time = time.perf_counter()

    while True:  # main loop
        cell_idx = unknowns[pointer]
        print(f'cell:{cell_idx} notes = {puzzle.notes[cell_idx]}')
        counter += 1
        if verbose:
            if counter % 10000 == 0 or counter == 0:
                # print(puzzle)
                t = time.perf_counter() - start_time
                known = puzzle.get_known_cells_count()
                print(f'counter {counter} time {t:0.1f} known: {known}\r', end="")

        if pointer == 0 and not np.any(puzzle.notes[cell_idx]):
            # We're back at the start, with no digits possible. 
            if verbose:
                print('puzzle has no solution!, counter ==', counter)
                break

        if not backtracking:
            pass

        if not np.any(puzzle.notes[cell_idx]):
            puzzle.cells[cell_idx] = 0
            pointer -= 1
            backtracking = True
            continue

        index = np.argmax(puzzle.notes[cell_idx])
        puzzle.notes[cell_idx][index] = False
        candidate = index + 1
        puzzle.cells[cell_idx] = candidate

        if puzzle.check_cell_is_valid(cell_idx):
            pointer += 1
            if pointer >= len(unknowns):
                return puzzle  # Puzzle is solved
            cell_idx = unknowns[pointer]
            puzzle.notes[cell_idx] = puzzle.calculate_notes_for_cell(cell_idx)
            backtracking = False
        else:
            puzzle.cells[cell_idx] = 0

    # We've broken out of the while loop - all possibilities explored
    return None
