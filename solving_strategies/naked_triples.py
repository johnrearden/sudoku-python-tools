from tools.constants import nonets, SolverResult
from tools.utils import recalculate_notes
from collections import defaultdict


def naked_triples(puzzle):
    for nonet in nonets:

        # Use a dictionary of lists, keyed by (ordered) pairs that appear, with
        # each list consisting of the cells in which this pair appears. If the
        # length of any list is 2, we have a pair appearing in 2 cells.
        triples_dict = defaultdict(list)
        for cell_index in nonet:
            notes = puzzle.notes[cell_index]
            if len(notes) == 3:
                ordered_notes = sorted(notes[:])
                triple = (ordered_notes[0], ordered_notes[1], ordered_notes[2])
                triples_dict[triple].append(cell_index)
        for triple in triples_dict:
            if len(triples_dict[triple]) == 3:
                triple_cells = triples_dict[triple]
                other_cells = [idx for idx in nonet if idx not in triple_cells]
                for cell_index in other_cells:
                    if puzzle.cells[cell_index] != 0:  # cell is already known
                        continue

                    # Remove the digits in the pair from all other cells
                    if triple[0] in puzzle.notes[cell_index]:
                        puzzle.notes[cell_index].remove(triple[0])
                    if triple[1] in puzzle.notes[cell_index]:
                        puzzle.notes[cell_index].remove(triple[1])
                    if triple[2] in puzzle.notes[cell_index]:
                        puzzle.notes[cell_index].remove(triple[2])
                    if len(puzzle.notes[cell_index]) == 1:
                        puzzle.cells[cell_index] = puzzle.notes[cell_index][0]
                        puzzle = recalculate_notes(puzzle)
                        return SolverResult.NOTES_AND_CELLS_CHANGED
    return SolverResult.NO_CHANGE
