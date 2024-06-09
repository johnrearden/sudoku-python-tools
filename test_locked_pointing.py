from solving_strategies.locked_candidates import locked_candidates_claiming
from tools.classes import Puzzle
from tools.utils import recalculate_notes, empty_notes_for_known_cells

if __name__ == '__main__':
    fruzzled_easy = '-387642--16---8-3-4791-26--3------2--2-34--51---25-4---13-275--6-7-1----25-6----7'
    puzzle = Puzzle()
    puzzle.build_from_string(fruzzled_easy)
    puzzle = recalculate_notes(puzzle)
    puzzle = empty_notes_for_known_cells(puzzle)
    result = locked_candidates_claiming(puzzle)
    