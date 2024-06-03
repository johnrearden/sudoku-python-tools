from tools.constants import nonets, SolverResult
from tools.utils import recalculate_notes
from collections import defaultdict
from itertools import combinations, chain


def hidden_triples(puzzle):
    for nonet in nonets:

        # Use a dictionary of lists, keyed by (ordered) triples that appear,
        # with each list consisting of the cells in which this triple appears.
        # If the length of any list is 2, we have a triple appearing in 2 cells
        triples_dict = defaultdict(list)
        for cell_index in nonet:
            notes = puzzle.notes[cell_index]
            all_triples = combinations(notes, 3)
            for triple in all_triples:
                triples_dict[triple].append(cell_index)

        for triple in triples_dict:
            if len(triples_dict[triple]) == 3:
                # Need to check that the digits in the tripl appear in no other
                # cell's notes
                triple_cells = triples_dict[triple]
                other_cells = [idx for idx in nonet if idx not in triple_cells]
                other_cells_notes = [puzzle.notes[idx] for idx in other_cells]
                notes_set = set(chain.from_iterable(other_cells_notes))

                if (triple[0] in notes_set
                        or triple[1] in notes_set
                        or triple[2] in notes_set):
                    continue  # this pair's digits appear elsewhere.

                # Remove all other digits from the 2 cells with the hidden
                # pairs
                for cell_index in triple_cells:
                    if len(puzzle.notes[cell_index]) == 3:
                        continue  # No extra digits exist to remove
                    puzzle.notes[cell_index] = list(triple)
                    puzzle = recalculate_notes(puzzle)
                    return SolverResult.NOTES_ONLY_CHANGED
    return SolverResult.NO_CHANGE
