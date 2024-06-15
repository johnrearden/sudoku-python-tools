from solving_strategies.brute_force import brute_force
from tools.uniqueness_test import is_unique
from tools.classes import Puzzle
from tools.utils import recalculate_notes

from collections import defaultdict
import csv


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
    known_count = len(knowns)

    results = []
        
    for i, idx in enumerate(knowns):
        print(f'{i + 1} of {known_count}')
        puzzle = Puzzle()
        puzzle.build_from_string(puzzle_string)
        puzzle.cells[idx] = 0
        puzzle = recalculate_notes(puzzle)
        new_puzzle_string = puzzle.to_short_string()

        unique = is_unique(puzzle)

        if unique:
            print(f'Removing cell {idx} from puzzle results in another'
                 f' valid puzzle')
            print(new_puzzle_string)
            results.append(new_puzzle_string)
        else:
            pass
            print(f'Removing cell {idx} from puzzle results in invalid puzzle')
            
    return results


if __name__ == '__main__':

    s = '-43----2--7-48----52---6----5-8--4----------------4657---63--4-495----8---754-1--'
    count = len([char for char in s if char != '-'])
    print(count)

    with open('1hr_run.csv') as file:

        csv_reader = csv.reader(file, delimiter=',')
        puzzle_dict = defaultdict(list)
        for row in csv_reader:
            key = int(row[0])
            puzzle_dict[key].append(row[1])

        further_puzzles = {}
        candidates = [puzzle_dict[27][3]]
        all_results = candidates[:]
        while candidates:
            results = try_every_removal(candidates.pop())
            candidates.extend(results)
            print(f'{len(candidates)} left, {len(all_results)} results')
            for result in results:
                known_count = len([char for char in result if char != '-'])
                further_puzzles[known_count] = result  # update with new
                print(f'{known_count},{result}')
            for key, value in further_puzzles.items():
                print(f'{key},{value}')
    

