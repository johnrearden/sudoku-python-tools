from tools.constants import nonets, nonets_for_cell, SolverResult
from tools.utils import recalculate_notes


def locked_candidates_pointing(puzzle):
    for digit in range(1, 10):
        # print('###############################')
        # print(f'##########   {digit}   ########')
        # print('###############################')
        for block in nonets[18:27]:
            tp_lft_cell = block[0]
            in_1 = False
            in_2 = False
            in_3 = False
            column_1 = [tp_lft_cell, tp_lft_cell + 9, tp_lft_cell + 18]
            column_2 = [tp_lft_cell + 1, tp_lft_cell + 10, tp_lft_cell + 19]
            column_3 = [tp_lft_cell + 2, tp_lft_cell + 11, tp_lft_cell + 20]
            # print('columns:', column_1, column_2, column_3)
            for cell_index in column_1:
                # print(f'notes for {cell_index}: {puzzle.notes[cell_index]}')
                if digit in puzzle.notes[cell_index]:
                    in_1 = True
            for cell_index in column_2:
                # print(f'notes for {cell_index}: {puzzle.notes[cell_index]}')
                if digit in puzzle.notes[cell_index]:
                    in_2 = True
            for cell_index in column_3:
                # print(f'notes for {cell_index}: {puzzle.notes[cell_index]}')
                if digit in puzzle.notes[cell_index]:
                    in_3 = True
            # print('ins:', in_1, in_2, in_3)
            one_note_removed = False
            if in_1 and not in_2 and not in_3:
                # print('in 1 only')
                nonet_index = nonets_for_cell[column_1[0]][1]
                col_nonet = nonets[nonet_index]
                other_cells = [idx for idx in col_nonet if idx not in column_1]
                # print('col_nonet', col_nonet)
                # print('other_cells', other_cells)
                for cell in other_cells:
                    if digit in puzzle.notes[cell]:
                        # print(f'removing {digit} from {cell} notes')
                        puzzle.notes[cell].remove(digit)
                        one_note_removed = True
            if not in_1 and in_2 and not in_3:
                # print('in 2 only')
                nonet_index = nonets_for_cell[column_2[0]][1]
                col_nonet = nonets[nonet_index]
                other_cells = [idx for idx in col_nonet if idx not in column_2]
                # print('col_nonet', col_nonet)
                # print('other_cells', other_cells)
                for cell in other_cells:
                    if digit in puzzle.notes[cell]:
                        # print(f'removing {digit} from {cell} notes')
                        puzzle.notes[cell].remove(digit)
                        one_note_removed = True
            if not in_1 and not in_2 and in_3:
                # print('in 3 only')
                nonet_index = nonets_for_cell[column_3[0]][1]
                col_nonet = nonets[nonet_index]
                other_cells = [idx for idx in col_nonet if idx not in column_3]
                # print('col_nonet', col_nonet)
                # print('other_cells', other_cells)
                for cell in other_cells:
                    if digit in puzzle.notes[cell]:
                        # print(f'removing {digit} from {cell} notes')
                        puzzle.notes[cell].remove(digit)
                        one_note_removed = True
            if one_note_removed:
                return SolverResult.NOTES_ONLY_CHANGED
    return SolverResult.NO_CHANGE
                    