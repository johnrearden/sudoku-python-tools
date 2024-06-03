from tools.constants import nonets, SolverResult
from tools.utils import recalculate_notes
from collections import defaultdict
from itertools import combinations, chain


def hidden_pairs(puzzle):
    for nonet in nonets:

        # Use a dictionary of lists, keyed by (ordered) pairs that appear, with
        # each list consisting of the cells in which this pair appears. If the
        # length of any list is 2, we have a pair appearing in 2 cells.
        pairs_dict = defaultdict(list)
        for cell_index in nonet:
            notes = puzzle.notes[cell_index]
            all_pairs = combinations(notes, 2)
            for pair in all_pairs:
                pairs_dict[pair].append(cell_index)

        for pair in pairs_dict:
            if len(pairs_dict[pair]) == 2:
                # Need to check that the digits in the pair appear in no other
                # cell's notes
                pair_cells = pairs_dict[pair]
                other_cells = [idx for idx in nonet if idx not in pair_cells]
                other_cells_notes = [puzzle.notes[idx] for idx in other_cells]
                notes_set = set(chain.from_iterable(other_cells_notes))

                if pair[0] in notes_set or pair[1] in notes_set:
                    continue  # this pair's digits appear elsewhere.

                # Remove all other digits from the 2 cells with the hidden
                # pairs
                for cell_index in pair_cells:
                    if len(puzzle.notes[cell_index]) == 2:
                        continue  # No extra digits exist to remove
                    puzzle.notes[cell_index] = list(pair)
                    puzzle = recalculate_notes(puzzle)
                    return SolverResult.NOTES_ONLY_CHANGED
    return SolverResult.NO_CHANGE
