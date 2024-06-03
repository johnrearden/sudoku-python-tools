from tools.constants import nonets, SolverResult
from tools.utils import recalculate_notes
from collections import defaultdict


def naked_pairs(puzzle):
    for nonet in nonets:
        
        # Use a dictionary of lists, keyed by (ordered) pairs that appear, with
        # each list consisting of the cells in which this pair appears. If the
        # length of any list is 2, we have a pair appearing in 2 cells.
        pairs_dict = defaultdict(list)
        for cell_index in nonet:
            notes = puzzle.notes[cell_index]
            if len(notes) == 2:
                ordered_notes = sorted(notes[:])
                pair = (ordered_notes[0], ordered_notes[1])
                pairs_dict[pair].append(cell_index)
        for pair in pairs_dict:
            if len(pairs_dict[pair]) == 2:
                pair_cells = pairs_dict[pair]
                other_cells = [idx for idx in nonet if idx not in pair_cells]
                for cell_index in other_cells:
                    if puzzle.cells[cell_index] != 0:  # cell is already known
                        continue

                    # Remove the digits in the pair from all other cells
                    if pair[0] in puzzle.notes[cell_index]:
                        puzzle.notes[cell_index].remove(pair[0])
                    if pair[1] in puzzle.notes[cell_index]:
                        puzzle.notes[cell_index].remove(pair[1])
                    if len(puzzle.notes[cell_index]) == 1:
                        puzzle.cells[cell_index] = puzzle.notes[cell_index][0]
                        puzzle = recalculate_notes(puzzle)
                        return SolverResult.NOTES_AND_CELLS_CHANGED
    return SolverResult.NO_CHANGE
