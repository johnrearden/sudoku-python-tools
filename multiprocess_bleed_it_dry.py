from tools.uniqueness_test import is_unique
from tools.classes import Puzzle
from tools.utils import recalculate_notes

from collections import defaultdict
from multiprocessing import Process, Queue, cpu_count
import csv
import queue
import time


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

    results = []

    for i, idx in enumerate(knowns):
        # print(f'{i + 1} of {known_count}')
        puzzle = Puzzle()
        puzzle.build_from_string(puzzle_string)
        puzzle.cells[idx] = 0
        puzzle = recalculate_notes(puzzle)
        new_puzzle_string = puzzle.to_short_string()

        unique = is_unique(puzzle)

        if unique:
            # print(
            #     f'Removing cell {idx} from puzzle results in another'
            #     f' valid puzzle'
            # )
            # print(new_puzzle_string)
            results.append(new_puzzle_string)
        else:
            pass
            # print(f'Removing cell {idx} results in invalid puzzle')

    return results


def examine_puzzle(tasks_to_do, completed_tasks):
    further_puzzles = {}
    while True:
        try:
            puzzle_string = tasks_to_do.get_nowait()
        except queue.Empty:
            break
        else:
            candidates = [puzzle_string]
            break_from_while = False
            while candidates:
                results = try_every_removal(candidates.pop())
                candidates.extend(results)
                for result in results:
                    known_count = len([char for char in result if char != '-'])
                    further_puzzles[known_count] = result  # update with new
                    if known_count == 23:
                        break_from_while = True
                if break_from_while:
                    break  # stop at 22, seems like less is wasted effort
            completed_tasks.put(further_puzzles)
    return True


if __name__ == '__main__':
    with open('1hr_run.csv') as file:
        csv_reader = csv.reader(file, delimiter=',')
        puzzle_dict = defaultdict(list)
        for row in csv_reader:
            key = int(row[0])
            puzzle_dict[key].append(row[1])

    start_time = time.perf_counter()
    number_of_processes = cpu_count()
    tasks_to_do = Queue()
    completed_tasks = Queue()
    processes = []

    # Start the Processes, number == cpu_count()
    candidates_with_27 = puzzle_dict[28]
    for cdt in candidates_with_27:
        tasks_to_do.put(cdt)
    num_tasks = len(candidates_with_27)
    for _ in range(number_of_processes):
        p = Process(
            target=examine_puzzle,
            args=(tasks_to_do, completed_tasks))
        processes.append(p)
        p.start()

    # While there are tasks outstanding, if there's a completed task in
    # the queue, grab it, get the puzzle with the minimum knows, and
    # write it to a results file
    while True:
        with open('tough_muddas.csv', 'a') as outfile:
            if not completed_tasks.empty():
                result_dict = completed_tasks.get()
                num_tasks -= 1
                min_key = min(result_dict.keys())
                min_result = result_dict[min_key]
                outfile.write(f'{min_key},{min_result}\n')
                time_elapsed = time.perf_counter() - start_time
                print(
                    f'Found: {min_key} : {min_result}\n'
                    f'{num_tasks} remaining\n'
                    f'time elapsed {time_elapsed:0.1f}s'
                )
                if num_tasks == 0:
                    break
            else:
                time.sleep(0.5)

    for p in processes:
        p.join()

    print(f'Duration : {time.perf_counter() - start_time}')
