import math
from tools.constants import nonets


def get_row(index):
    start = math.floor(index / 9) * 9
    row = []
    for i in range(start, start + 9):
        row.append(i)
    return row


def get_column(index):
    start = index % 9
    col = []
    for j in range(start, 81, 9):
        col.append(j)
    return col


def get_square(index):
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


