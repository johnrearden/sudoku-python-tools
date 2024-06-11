from tools.classes import NpPuzzle, Puzzle
from solving_strategies.np_brute_force import np_brute_force
from solving_strategies.brute_force import brute_force

from time import perf_counter


if __name__ == '__main__':
    ps = (
        '''--569-----3------9--8----1-'''
        '''47--3----1----4--8-----7---'''
        '''------471---2--3-----3-58--'''
    )
    puzzle = NpPuzzle()
    puzzle.build_from_string(ps)

    start_time = perf_counter()
    solution = np_brute_force(puzzle, verbose=True)
    print(solution)
    print('np_brute_force:', perf_counter() - start_time)
    
    puzzle = Puzzle()
    puzzle.build_from_string(ps)
    start_time = perf_counter()
    solution = brute_force(puzzle)
    print(solution)
    print('brute_force:', perf_counter() - start_time)
