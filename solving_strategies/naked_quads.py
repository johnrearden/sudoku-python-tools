from tools.constants import nonets, SolverResult
from tools.utils import recalculate_notes
from collections import defaultdict


def naked_quads(puzzle):
    for nonet in nonets:

        # Use a dictionary of lists, keyed by (ordered) pairs that appear, with
        # each list consisting of the cells in which this pair appears. If the
        # length of any list is 4, we have a pair appearing in 4 cells.
        quads_dict = defaultdict(list)
        for cell_index in nonet:
            notes = puzzle.notes[cell_index]
            if len(notes) == 4:
                ordered_notes = sorted(notes[:])
                quad = (
                    ordered_notes[0],
                    ordered_notes[1],
                    ordered_notes[2],
                    ordered_notes[3]
                )
                quads_dict[quad].append(cell_index)
        for quad in quads_dict:
            if len(quads_dict[quad]) == 4:  # these 4 notes appear in 4 cells
                quads_cells = quads_dict[quad]
                other_cells = [idx for idx in nonet if idx not in quads_cells]
                for cell_index in other_cells:
                    if puzzle.cells[cell_index] != 0:  # cell is already known
                        continue

                    # Remove the digits in the quad from all other cells
                    if quad[0] in puzzle.notes[cell_index]:
                        puzzle.notes[cell_index].remove(quad[0])
                    if quad[1] in puzzle.notes[cell_index]:
                        puzzle.notes[cell_index].remove(quad[1])
                    if quad[2] in puzzle.notes[cell_index]:
                        puzzle.notes[cell_index].remove(quad[2])
                    if quad[3] in puzzle.notes[cell_index]:
                        puzzle.notes[cell_index].remove(quad[3])
                    if len(puzzle.notes[cell_index]) == 1:
                        puzzle.cells[cell_index] = puzzle.notes[cell_index][0]
                        puzzle = recalculate_notes(puzzle)
                        return SolverResult.NOTES_AND_CELLS_CHANGED
    return SolverResult.NO_CHANGE
