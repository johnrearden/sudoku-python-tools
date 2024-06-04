from tools.constants import nonets, SolverResult
from collections import defaultdict
from tools.utils import recalculate_notes


def hidden_single(puzzle, updatePuzzle=True):
    """
    This solving method iterates through the nonets, and works out for each
    nonet how many of the cells have each digit as a possibility.

    If a digit appears only once in this dictionary of cells, then it can
    only be in one cell. The last occurrence (only occurence in this case) of
    the digit in a cell is recorded, and the cell is set to that digit.

    The method returns at this point, because the puzzle notes need to be
    updated.
    """

    for nonet in nonets:
        print_it = False
        if print_it:
            print(nonet)
        possibles = [n for n in range(1, 10)]
        existing_digits = []
        unknown_cells = []

        for idx in nonet:
            if puzzle.cells[idx] == 0:
                unknown_cells.append(idx)
            else:
                existing_digits.append(puzzle.cells[idx])
        if print_it:
            print('unknown_cells', unknown_cells)
            print('existing_digits', existing_digits)

        missing_digits = [n for n in possibles if n not in existing_digits]
        occurences = defaultdict(int)
        for n in range(1, 10):
            occurences[n]
        last_occurences = {}

        for cell in unknown_cells:
            missing_from_cell = puzzle.notes[cell]
            for digit in missing_digits:
                if digit in missing_from_cell:
                    occurences[digit] += 1
                    last_occurences[digit] = cell

        if print_it:
            print('occurences:', occurences)

        for digit, count in occurences.items():
            if count == 1:
                cell = last_occurences[digit]
                puzzle.cells[cell] = digit
                puzzle = recalculate_notes(puzzle)
                return SolverResult.NOTES_AND_CELLS_CHANGED  # notes need to be recalculated

    return SolverResult.NO_CHANGE  # solving method unsuccessful for all nonets
