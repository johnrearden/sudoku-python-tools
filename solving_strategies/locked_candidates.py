from tools.constants import nonets, nonets_for_cell, SolverResult
from collections import defaultdict


def locked_candidates_pointing(puzzle):

    # Examine columns in squares first. If the digit only appears in one
    # column, and not the others, then it must be in these cells and not
    # elsewhere in that same column, outside the square.

    for digit in range(1, 10):
        one_note_removed = False
        for block in nonets[18:27]:  # the squares
            tp_lft_cell = block[0]
            in_1 = False
            in_2 = False
            in_3 = False
            column_1 = [tp_lft_cell, tp_lft_cell + 9, tp_lft_cell + 18]
            column_2 = [tp_lft_cell + 1, tp_lft_cell + 10, tp_lft_cell + 19]
            column_3 = [tp_lft_cell + 2, tp_lft_cell + 11, tp_lft_cell + 20]
            for cell_index in column_1:
                if digit in puzzle.notes[cell_index]:
                    in_1 = True
            for cell_index in column_2:
                if digit in puzzle.notes[cell_index]:
                    in_2 = True
            for cell_index in column_3:
                if digit in puzzle.notes[cell_index]:
                    in_3 = True

            # Remove the digit from the notes of other cells in the column.
            if in_1 and not in_2 and not in_3:
                nonet_index = nonets_for_cell[column_1[0]][1]
                col_nonet = nonets[nonet_index]
                other_cells = [idx for idx in col_nonet if idx not in column_1]
                for cell in other_cells:
                    if digit in puzzle.notes[cell]:
                        puzzle.notes[cell].remove(digit)
                        one_note_removed = True
            if not in_1 and in_2 and not in_3:
                nonet_index = nonets_for_cell[column_2[0]][1]
                col_nonet = nonets[nonet_index]
                other_cells = [idx for idx in col_nonet if idx not in column_2]
                for cell in other_cells:
                    if digit in puzzle.notes[cell]:
                        puzzle.notes[cell].remove(digit)
                        one_note_removed = True
            if not in_1 and not in_2 and in_3:
                nonet_index = nonets_for_cell[column_3[0]][1]
                col_nonet = nonets[nonet_index]
                other_cells = [idx for idx in col_nonet if idx not in column_3]
                for cell in other_cells:
                    if digit in puzzle.notes[cell]:
                        puzzle.notes[cell].remove(digit)
                        one_note_removed = True
            if one_note_removed:
                return SolverResult.NOTES_ONLY_CHANGED

    # Next, examine rows in squares
    for digit in range(1, 10):
        for block in nonets[18:27]:
            tp_lft_cell = block[0]
            in_1 = False
            in_2 = False
            in_3 = False
            row_1 = [tp_lft_cell, tp_lft_cell + 1, tp_lft_cell + 2]
            row_2 = [tp_lft_cell + 9, tp_lft_cell + 10, tp_lft_cell + 11]
            row_3 = [tp_lft_cell + 18, tp_lft_cell + 19, tp_lft_cell + 20]
            for cell_index in row_1:
                if digit in puzzle.notes[cell_index]:
                    in_1 = True
            for cell_index in row_2:
                if digit in puzzle.notes[cell_index]:
                    in_2 = True
            for cell_index in row_3:
                if digit in puzzle.notes[cell_index]:
                    in_3 = True
            one_note_removed = False
            if in_1 and not in_2 and not in_3:
                nonet_index = nonets_for_cell[row_1[0]][0]
                row_nonet = nonets[nonet_index]
                other_cells = [idx for idx in row_nonet if idx not in row_1]
                for cell in other_cells:
                    if digit in puzzle.notes[cell]:
                        puzzle.notes[cell].remove(digit)
                        one_note_removed = True
            if not in_1 and in_2 and not in_3:
                nonet_index = nonets_for_cell[row_2[0]][0]
                row_nonet = nonets[nonet_index]
                other_cells = [idx for idx in row_nonet if idx not in row_2]
                for cell in other_cells:
                    if digit in puzzle.notes[cell]:
                        puzzle.notes[cell].remove(digit)
                        one_note_removed = True
            if not in_1 and not in_2 and in_3:
                nonet_index = nonets_for_cell[row_3[0]][0]
                row_nonet = nonets[nonet_index]
                other_cells = [idx for idx in row_nonet if idx not in row_3]
                for cell in other_cells:
                    if digit in puzzle.notes[cell]:
                        puzzle.notes[cell].remove(digit)
                        one_note_removed = True
            if one_note_removed:
                return SolverResult.NOTES_ONLY_CHANGED

    return SolverResult.NO_CHANGE


def locked_candidates_claiming(puzzle):
    one_note_removed = False
    for digit in range(1, 10):
        # print('*******************************')
        # print(f'********* {digit} *************')
        # print('*******************************')
        for nonet in nonets[0:9]:  # Explore rows first.
            # print(f'nonet : {nonet}')
            cell_squares = defaultdict(list)
            for cell_index in nonet:
                if digit in puzzle.notes[cell_index]:
                    sqr_index = nonets_for_cell[cell_index][2]
                    cell_squares[sqr_index].append(cell_index)
            if len(cell_squares) == 1:
                square = list(cell_squares.keys())[0]
                # print('cell_squares:', cell_squares)
                # Get the other cells in this square that are not in the row.
                other_cells = [i for i in nonets[square] if i not in nonet]
                # print('others', other_cells)
                for idx in other_cells:
                    if digit in puzzle.notes[idx]:
                        puzzle.notes[idx].remove(digit)
                        # print(f'{digit} removed from notes for cell {idx}')
                        one_note_removed = True
            if one_note_removed:
                return SolverResult.NOTES_ONLY_CHANGED

    # If no result from rows, explore columns
    for digit in range(1, 10):
        for nonet in nonets[9:18]:  # Explore columns next.
            cell_squares = defaultdict(list)
            for cell_index in nonet:
                if digit in puzzle.notes[cell_index]:
                    sqr_index = nonets_for_cell[cell_index][2]
                    cell_squares[sqr_index].append(cell_index)

            # If the digit only appears in the column cell in this square, and
            # nowhere else in the column, then it can't be elsewhere in the
            # square. Remove it from the notes of other cells in the square.
            if len(cell_squares) == 1:
                square = list(cell_squares.keys())[0]
                other_cells = [i for i in nonets[square] if i not in nonet]
                for idx in other_cells:
                    if digit in puzzle.notes[idx]:
                        puzzle.notes[idx].remove(digit)
                        one_note_removed = True
            if one_note_removed:
                return SolverResult.NOTES_ONLY_CHANGED

    return SolverResult.NO_CHANGE
