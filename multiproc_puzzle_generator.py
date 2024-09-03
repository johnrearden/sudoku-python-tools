import random
import time
import argparse
from multiprocessing import Process, Queue, cpu_count, Value

from tools.classes import Puzzle
from tools.utils import choose_n_unknowns
from tools.uniqueness_test import is_unique
from solving_strategies.brute_force import brute_force


def create_sudoku_puzzle(target, completed_tasks, go_flag):
    """
    A completed puzzle is created, and then cells removed one by one (but not
    reducing the number of unknowns to more than one digit below 1). If at any
    point the puzzle not longer has a unique solution, it is abandoned.
    """
    while go_flag.value:  # Continue until the go_flag is set to False

        puzzle = Puzzle()
        brute_force(puzzle)     

        indices_to_remove = choose_n_unknowns(puzzle, 81 - target)
        random.shuffle(indices_to_remove)

        # Main digit removal loop
        valid_result = True
        for cell in indices_to_remove:
            puzzle.cells[cell] = 0
            clone = puzzle.clone()
            unique = is_unique(clone)
            if not unique:
                valid_result = False
                break

        if valid_result:
            result = f'{puzzle.knowns_count()},{puzzle.to_short_string()}'
            completed_tasks.put(result)

    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t', '--time',
        type=int,
        default=10,
        help='Number of seconds to run the process'
    )
    parser.add_argument(
        '-k', '--knowns',
        type=int,
        default=30,
        help='Number of knowns in the puzzle'
    )
    args = parser.parse_args()
    target_count = args.knowns
    run_time = args.time
    num_processes = cpu_count()
    print(f'Starting the processes using {num_processes} cores')
    completed_tasks = Queue()
    start_time = time.perf_counter()
    processes = []
    num_found = 0

    # Start the processes
    go_flag = Value('b', True)
    for _ in range(num_processes):
        process = Process(
            target=create_sudoku_puzzle,
            args=(target_count, completed_tasks, go_flag)
        )
        processes.append(process)
        process.start()

    filename = f'data/generated_puzzles/{target_count}_knowns.csv'
    with open(filename, 'a') as file:
        while time.perf_counter() - start_time < run_time:
            if not completed_tasks.empty():
                result = completed_tasks.get()
                num_found += 1
                time_elapsed = time.perf_counter() - start_time
                out = (
                    f'{num_found} ({target_count}) found in '
                    f'{time_elapsed:.2f}s        ')
                print(out + '\r', end='')
                file.write(result + '\n')
                file.flush()
            else:
                time.sleep(0.1)

    go_flag.value = False
    for proc in processes:
        proc.join()

    print(f'Found {num_found} puzzles in {run_time} seconds')


if __name__ == '__main__':
    main()
