from collections import defaultdict

from tools.constants import nonets
from tools.constants import SolverResult


def x_wing_rows(puzzle):
    all_rows = nonets[:9]
    for digit in range(7, 8):
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
                for row in other_rows:
                    if digit in puzzle.notes[row[first_col]]:
                        puzzle.notes[row[first_col]].remove(digit)
                    if digit in puzzle.notes[row[second_col]]:
                        puzzle.notes[row[second_col]].remove(digit)
                return SolverResult.NOTES_ONLY_CHANGED

            # print(f'Notes for cols {first_col} & {second_col} after')
            # for row in all_rows:
            #     print(puzzle.notes[row[first_col]], puzzle.notes[row[second_col]])
    return SolverResult.NO_CHANGE