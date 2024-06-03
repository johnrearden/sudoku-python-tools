from tools.utils import get_column, get_row, get_square, recalculate_notes
from tools.constants import SolverResult


def one_per_nonet(puzzle, update_puzzle=True):

    change_detected = SolverResult.NO_CHANGE

    for index, cell in enumerate(puzzle.cells):
        row = get_row(index)
        col = get_column(index)
        sqr = get_square(index)

        row_numbers = [puzzle.cells[n] for n in row if puzzle.cells[n] > 0]
        col_numbers = [puzzle.cells[n] for n in col if puzzle.cells[n] > 0]
        sqr_numbers = [puzzle.cells[n] for n in sqr if puzzle.cells[n] > 0]

        number_set = set([*row_numbers, *col_numbers, *sqr_numbers])
        number_list = list(number_set)
        for num in number_list:
            if num in puzzle.notes[index] and num != cell:
                puzzle.notes[index].remove(num)
                
    if update_puzzle:
        for index, cell in enumerate(puzzle.cells):
            if len(puzzle.notes[index]) == 1 and puzzle.cells[index] == 0:
                puzzle.cells[index] = puzzle.notes[index][0]
                change_detected = SolverResult.NOTES_AND_CELLS_CHANGED
                puzzle = recalculate_notes(puzzle)
                
    return change_detected
            

        
        