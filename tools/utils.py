import math
from tools.constants import nonets


def get_row(index):
    """
    Returns the indices of the cells that share a row with the cell at the
    specified index.
    """
    start = math.floor(index / 9) * 9
    row = []
    for i in range(start, start + 9):
        row.append(i)
    return row


def get_column(index):
    """
    Returns the indices of the cells that share a column with the cell at the
    specified index.
    """
    start = index % 9
    col = []
    for j in range(start, 81, 9):
        col.append(j)
    return col


def get_square(index):
    """
    Returns the indices of the cells that share a square with the cell at the
    specified index.
    """
    temp = math.floor(index / 9)
    indexMod9 = index % 9
    iStart = indexMod9 - (indexMod9 % 3)
    jStart = temp - (temp % 3)

    square = []

    for i in range(iStart, iStart + 3):
        for j in range(jStart, jStart + 3):
            square.append(j * 9 + i)
    return square


def check_puzzle_validity(puzzle):
    """
    Method runs through each nonet, and ensures that no cell value is
    duplicated.
    """
    assert len(puzzle.cells) == 81, "Puzzle should have 81 cells!"

    for nonet in nonets:
        values = []
        for idx in nonet:
            cell_value = puzzle.cells[idx]
            if cell_value in values:
                return False
            else:
                if cell_value > 0:
                    values.append(cell_value)

    return True


def check_cell_validity(cell_index, puzzle):
    """
    Method checks the row, column and square that the specified cell is in, 
    to ensure that the digit in the cell is not replicated in any of these 3
    nonets.
    """
    cell_value = puzzle.cells[cell_index]

    row = [idx for idx in get_row(cell_index) if idx != cell_index]
    col = [idx for idx in get_column(cell_index) if idx != cell_index]
    sqr = [idx for idx in get_square(cell_index) if idx != cell_index]
    all_cells = list(set([*row, *col, *sqr])) # combine w/o duplicates
    all_digits = [puzzle.cells[idx] for idx in all_cells]

    if cell_value in all_digits:
        return False
    return True




