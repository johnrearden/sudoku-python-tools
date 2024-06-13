from solving_strategies.brute_force import brute_force
from tools.classes import Puzzle
from tools.uniqueness_test import is_unique
import time


def main():
    while True:
        msg = 'Enter your puzzle as a string, using "-" to represent a blank\n'
        puzzle_string = input(msg)
        if len(puzzle_string) == 81:
            break

    # Solve the puzzle
    puzzle = Puzzle()
    puzzle.build_from_string(puzzle_string)
    original = puzzle.clone()

    start_time = time.perf_counter()
    puzzle = brute_force(puzzle)
    duration = time.perf_counter() - start_time
    print(puzzle)
    print(f'puzzle solved in {duration:0.3f} seconds')
    print('checking uniqueness ..........')

    unique = is_unique(original)
    if unique:
        print('Puzzle has a unique solution')
    else:
        print('Puzzle has either no solution or multiple solutions')


if __name__ == '__main__':
    main()
