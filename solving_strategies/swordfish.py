from collections import defaultdict
from itertools import combinations

from tools.constants import nonets
from tools.constants import SolverResult


def swordfish_rows(puzzle):
    all_rows = nonets[:9]
    for digit in range(1, 10):
        # print('***********')
        # print(digit)
        # print('***********')
        freq_dict = defaultdict(list)
        for row_number, row in enumerate(all_rows):
            for cell in row:
                col_number = cell % 9
                if digit in puzzle.notes[cell]:
                    freq_dict[row_number].append(col_number)
        # print(freq_dict)
        rows_with_2_or_3_cols = {}
        for row_number in freq_dict:
            num_cols = len(freq_dict[row_number])
            if num_cols == 2 or num_cols == 3:
                rows_with_2_or_3_cols[row_number] = freq_dict[row_number]
        # print(rows_with_2_or_3_cols.keys())

        row_combos = combinations(rows_with_2_or_3_cols.keys(), 3)
        pruned_row_combos = defaultdict(list)
        for combo in row_combos:
            cols_appearing_twice_or_more = 0
            col_appearances = defaultdict(int)
            col_list = []
            for row in combo:
                for col in rows_with_2_or_3_cols[row]:
                    col_appearances[col] += 1
                    if col_appearances[col] == 2:
                        cols_appearing_twice_or_more += 1
                    if col_appearances[col] == 1:
                        col_list.append(col)
            if cols_appearing_twice_or_more >= 3 and len(col_list) <= 3:
                pruned_row_combos[combo] = col_list
                # print(f'{combo}: {col_appearances}')
                # print(f'{combo}: {col_list}')

        # print()
        # print(f'{digit} : pruned row combos :')
        # for combo in pruned_row_combos:
        #     print(digit, combo, pruned_row_combos[combo])

        # There should only be 1 set of 3 rows.
        if len(pruned_row_combos) > 1:
            # print('len(pruned_row_combos) > 1')
            return SolverResult.NO_CHANGE

        # Remove the digit from the notes of the cover cells.
        at_least_one_removed = False
        if pruned_row_combos:
            for row_combo, col_list in pruned_row_combos.items():  # Only 1
                other_rows = [n for n in range(0, 9) if n not in row_combo]
                for row in other_rows:
                    for col in col_list:
                        cell_idx = col + (row * 9)
                        if digit in puzzle.notes[cell_idx]:
                            puzzle.notes[cell_idx].remove(digit)
                            at_least_one_removed = True
                            # print(f'removing {digit} from {cell_idx}')
            if at_least_one_removed:
                # print('swordfish successful')
                return SolverResult.NOTES_ONLY_CHANGED

    return SolverResult.NO_CHANGE


def swordfish_cols(puzzle):
    all_cols = nonets[9:18]
    for digit in range(1, 10):
        # print('***********')
        # print(digit)
        # print('***********')
        freq_dict = defaultdict(list)
        for col_number, col in enumerate(all_cols):
            for cell in col:
                row_number = cell // 9
                if digit in puzzle.notes[cell]:
                    freq_dict[col_number].append(row_number)
        # print(freq_dict)
        cols_with_2_or_3_rows = {}
        for col_number in freq_dict:
            num_rows = len(freq_dict[col_number])
            if num_rows == 2 or num_rows == 3:
                cols_with_2_or_3_rows[col_number] = freq_dict[col_number]
        # print(cols_with_2_or_3_rows.keys())

        col_combos = combinations(cols_with_2_or_3_rows.keys(), 3)
        pruned_col_combos = defaultdict(list)
        for combo in col_combos:
            rows_appearing_twice_or_more = 0
            row_appearances = defaultdict(int)
            row_list = []
            for col in combo:
                for row in cols_with_2_or_3_rows[col]:
                    row_appearances[row] += 1
                    if row_appearances[row] == 2:
                        rows_appearing_twice_or_more += 1
                    if row_appearances[row] == 1:
                        row_list.append(row)
            if rows_appearing_twice_or_more >= 3 and len(row_list) <= 3:
                pruned_col_combos[combo] = row_list
                # print(f'{combo}: {row_appearances}')
                # print(f'{combo}: {row_list}')

        # print()
        # print(f'{digit} : pruned col combos :')
        # for combo in pruned_col_combos:
        #     print(digit, combo, pruned_col_combos[combo])

        # There should only be 1 set of 3 rows.
        if len(pruned_col_combos) > 1:
            # print('len(pruned_col_combos) > 1')
            return SolverResult.NO_CHANGE

        # Remove the digit from the notes of the cover cells.
        at_least_one_removed = False
        if pruned_col_combos:
            for col_combo, row_list in pruned_col_combos.items():  # Only 1
                other_cols = [n for n in range(0, 9) if n not in col_combo]
                for col in other_cols:
                    for row in row_list:
                        cell_idx = col + (row * 9)
                        if digit in puzzle.notes[cell_idx]:
                            puzzle.notes[cell_idx].remove(digit)
                            at_least_one_removed = True
                            # print(f'removing {digit} from {cell_idx}')
            if at_least_one_removed:
                # print('swordfish successful')
                return SolverResult.NOTES_ONLY_CHANGED

    return SolverResult.NO_CHANGE
