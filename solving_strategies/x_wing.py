from collections import defaultdict

from tools.constants import nonets
from tools.constants import SolverResult

import sys


def x_wing_rows(puzzle):
    all_rows = nonets[:9]
    for digit in range(1, 10):
        freq_dict = defaultdict(list)
        for row_number, row in enumerate(all_rows):
            for cell in row:
                col_number = cell % 9
                if digit in puzzle.notes[cell]:
                    freq_dict[row_number].append(col_number)
        ##print(freq_dict)
        rows_with_2_digits = {}
        for row_number in freq_dict:
            if len(freq_dict[row_number]) == 2:
                rows_with_2_digits[row_number] = freq_dict[row_number]
        #print(rows_with_2_digits)
        
        if len(rows_with_2_digits) == 2:  # Appears in only 2 rows
            cols = [cols for cols in rows_with_2_digits.values()]
            first_col = cols[0][0]
            second_col = cols[0][1]
            # print(cols)
            # print(first_col, second_col)
            
            #temp check
            # print(f'Notes for cols {first_col} & {second_col} before')
            # for row in all_rows:
            #     print(puzzle.notes[row[first_col]], puzzle.notes[row[second_col]])
            
            if cols[0] == cols[1]:  # Appears in the same cols in both rows
                # print(f'digit {digit} appears twice in 2 rows only - {rows_with_2_digits.keys()}, in columns {cols[0]}')
                # Remove the digit from the notes in the same 2 columns of
                # all the other rows.
                rows = [row for row in rows_with_2_digits.keys()]
                other_rows = [all_rows[n] for n in range(9) if n not in rows]
                some_note_removed = False
                for row in other_rows:
                    if digit in puzzle.notes[row[first_col]]:
                        puzzle.notes[row[first_col]].remove(digit)
                        some_note_removed = True
                    if digit in puzzle.notes[row[second_col]]:
                        puzzle.notes[row[second_col]].remove(digit)
                        some_note_removed = True
                if some_note_removed:
                    return SolverResult.NOTES_ONLY_CHANGED

            # print(f'Notes for cols {first_col} & {second_col} after')
            # for row in all_rows:
            #     print(puzzle.notes[row[first_col]], puzzle.notes[row[second_col]])
    return SolverResult.NO_CHANGE


def x_wing_cols(puzzle):
    all_cols = nonets[9:18]
    for digit in range(1, 10):
        freq_dict = defaultdict(list)
        for col_number, col in enumerate(all_cols):
            for cell in col:
                row_number = cell // 9
                if digit in puzzle.notes[cell]:
                    freq_dict[col_number].append(row_number)
        # print(digit, ' frequency:', freq_dict)
        cols_with_2_digits = {}
        for col_number in freq_dict:
            if len(freq_dict[col_number]) == 2:
                cols_with_2_digits[col_number] = freq_dict[col_number]
        # print('cols_with_2_digits', cols_with_2_digits)

        if len(cols_with_2_digits) == 2:
            rows = [rows for rows in cols_with_2_digits.values()]
            first_row = rows[0][0]
            second_row = rows[0][1]
            # print(rows)
            # print(first_row, second_row)

            if rows[0] == rows[1]:
                cols = [col for col in cols_with_2_digits.keys()]
                other_cols = [all_cols[n] for n in range(9) if n not in cols]
                some_note_removed = False
                for col in other_cols:
                    if digit in puzzle.notes[col[first_row]]:
                        puzzle.notes[col[first_row]].remove(digit)
                        some_note_removed = True
                    if digit in puzzle.notes[col[second_row]]:
                        puzzle.notes[col[second_row]].remove(digit)
                        some_note_removed = True
                if some_note_removed:
                    return SolverResult.NOTES_ONLY_CHANGED

            # print(f'Notes for cols {first_row} & {second_row} after')
            # for col in all_cols:
                # print(
                #     puzzle.notes[col[first_row]],
                #     puzzle.notes[col[second_row]])

    return SolverResult.NO_CHANGE
