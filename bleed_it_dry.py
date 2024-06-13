from solving_strategies.brute_force import brute_force
from tools.uniqueness_test import is_unique
from tools.classes import Puzzle
from tools.utils import recalculate_notes


def try_every_removal(puzzle_string):
    """
    Function takes a puzzle that has already been reduced to a small
    number of knowns (approaching the computational limit of the current
    algorithm) and tests removing every one of the remaining knowns. 

    This approach is computationally unrealistic for higher levels of knowns,
    but it would be a waste not to explore fully the sub-30 knowns puzzles that
    all the CPU cycles have been burnt on.
    """

    original = Puzzle()
    original.build_from_string(puzzle_string)
    knowns = [idx for idx in range(81) if original.cells[idx] > 0]
    print(knowns)

    for idx in knowns:
        print(idx)
        puzzle = Puzzle()
        puzzle.build_from_string(puzzle_string)
        puzzle.cells[idx] = 0
        puzzle = recalculate_notes(puzzle)
        new_puzzle_string = puzzle.to_short_string()

        unique = is_unique(puzzle)

        if unique:
            print(f'Removing cell {idx} from puzzle results in another'
                  f'valid puzzle')
            print(new_puzzle_string)
        else:
            print(f'Removing cell {idx} from puzzle result in invalid puzzle')


if __name__ == '__main__':
    puzzle_string = '-2--------5-8-76----49-6--8--6--9-7-3-7-5-----956---3--4-5--2--------76------3-5-'
    puzzle_string = '-2--------5-8-7-----49-6--8--6--9-7-3-7-5-----956---3--4-5--2--------76------3-5-'
    try_every_removal(puzzle_string)