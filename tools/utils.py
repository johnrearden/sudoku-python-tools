import math
import random
from collections import defaultdict
from tools.constants import nonets, nonets_for_cell


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
    all_cells = list(set([*row, *col, *sqr]))  # combine w/o duplicates
    all_digits = [puzzle.cells[idx] for idx in all_cells]

    if cell_value in all_digits:
        return False
    return True


def recalculate_notes(puzzle):
    """
    Method runs through each cell, eliminating any new digits that are not
    accounted for in the notes in each of the cell's row, column and square.

    It removes digits only, does not start from a full set of possible digits.
    """

    for index, cell in enumerate(puzzle.cells):
        notes = puzzle.notes[index]
        if cell != 0:
            notes = []
        else:
            row = get_row(index)
            row_digits = [puzzle.cells[i] for i in row]
            col = get_column(index)
            col_digits = [puzzle.cells[i] for i in col]
            sqr = get_square(index)
            sqr_digits = [puzzle.cells[i] for i in sqr]

            digits = set([*row_digits, *col_digits, *sqr_digits])
            notes = [n for n in notes if n not in digits]
        puzzle.notes[index] = notes

    return puzzle


def empty_notes_for_known_cells(puzzle):
    for i in range(0, 81):
        if puzzle.cells[i] != 0:
            puzzle.notes[i] = []
    return puzzle


def recalculate_cell_notes(cell_index, puzzle):
    nonets_to_check = [nonets[n] for n in nonets_for_cell[cell_index]]
    possibles = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
    actuals = set()
    for nonet in nonets_to_check:
        for idx in nonet:
            cell_value = puzzle.cells[idx]
            if cell_value != 0:
                actuals.add(cell_value)
    #print('actuals for cell :', cell_index, ' = ', actuals)
    remaining = possibles - actuals
    #print('remaining: ', remaining)
    return list(remaining)


def puzzle_complete(puzzle):
    unknowns = [puzzle.cells[i] for i in range(81) if puzzle.cells[i] == 0]
    puzzle_is_legal = check_puzzle_validity(puzzle)

    return not unknowns and puzzle_is_legal


def choose_n_unknowns(
        puzzle,
        unknowns_count,
        require_one_of_each_digit=False,
        should_sort=True):

    # The list to return
    unknown_cell_indices = []

    # Create bucket for each digit with cells containing that digit.
    buckets = defaultdict(list)
    for idx, cell_value in enumerate(puzzle.cells):
        assert cell_value >= 1 and cell_value <= 9, 'Values must lie 1 <= value <= 9'
        buckets[cell_value].append(idx)

    for bucket_key in buckets:
        random.shuffle(buckets[bucket_key])

    allow_empty_bucket = True and not require_one_of_each_digit
    removed_buckets = []
    for _ in range(unknowns_count):
        bucket_choice = random.choice(list(buckets.keys()))
        # print(buckets.keys())
        chosen_bucket = buckets[bucket_choice]
        # print(bucket_choice, chosen_bucket)
        unknown_cell_indices.append(chosen_bucket.pop())

        if len(chosen_bucket) <= 1 and not allow_empty_bucket:
            removed_buckets.append(bucket_choice)
            del buckets[bucket_choice]
            # print(f'---------length of bucket {bucket_choice} is 1, removing')
            # print(buckets.keys())

        if len(chosen_bucket) == 0 and allow_empty_bucket:
            allow_empty_bucket = False
            removed_buckets.append(bucket_choice)
            del buckets[bucket_choice]
            # print(f'---------length of bucket {bucket_choice} is 0, removing')
            # print(buckets.keys())

    # for k,v in buckets.items():
    #     print(k, v)
    # print(f'keys remaining: {len(buckets)}')
    # print(f'removed buckets: {removed_buckets}')
    # print(f'unknowns: {unknown_cell_indices}')
    if should_sort:
        return sorted(unknown_cell_indices)
    else:
        return unknown_cell_indices


def populate_digit_map(puzzle):
    digit_map = defaultdict(list)
    for idx, cell in enumerate(puzzle.cells):
        if cell != 0:
            digit_map[cell].append(idx)
    # for k, v in digit_map.items():
    #     print(k, v)
    if len(digit_map) < 9:
        keys_to_remove = []
        for digit, arr in digit_map.items():
            if len(arr) <= 1:
                keys_to_remove.append(digit)
        for digit in keys_to_remove:
            del digit_map[digit]
    
    # Shuffle each array of cell indices now, to allow client to pop() them.
    for v in digit_map.values():
        random.shuffle(v)
    # for k, v in digit_map.items():
    #     print(k, v)
    return digit_map


def get_puzzle_cells_as_string(puzzle):
    chars = [str(value) for value in puzzle.cells]
    return ''.join(chars).replace('0', '-')
