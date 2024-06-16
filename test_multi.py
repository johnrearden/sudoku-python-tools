from multiprocessing import Process, Queue, current_process, cpu_count
import queue
import time
import csv

from solving_strategies.brute_force import brute_force
from tools.classes import Puzzle


def do_job(tasks_to_do, completed_tasks):
    while True:
        try:
            puzzle_string = tasks_to_do.get_nowait()
        except queue.Empty:
            break
        else:
            puzzle = Puzzle()
            puzzle.build_from_string(puzzle_string)
            solution = brute_force(puzzle)
            if solution:
                completed_tasks.put(solution.to_short_string())
    return True


def main():
    start_time = time.perf_counter()
    number_of_processes = cpu_count()
    tasks_to_do = Queue()
    completed_tasks = Queue()
    processes = []
    num_tasks = 0

    with open('1hr_run.csv', 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            tasks_to_do.put(row[1])
            num_tasks += 1

    for w in range(number_of_processes):
        p = Process(target=do_job, args=(tasks_to_do, completed_tasks))
        processes.append(p)
        p.start()

    while True:
        with open('results_test.txt', 'a') as outfile:
            if not completed_tasks.empty():
                result = completed_tasks.get()
                print(result)
                outfile.write(f'{result}\n')
                num_tasks -= 1
                print(f'tasks remaining: {num_tasks}')
                if num_tasks == 0:
                    break
            else:
                time.sleep(.1)  # Poll every 10th of a second

    for p in processes:
        p.join()

    while not completed_tasks.empty():
        print(completed_tasks.get())
        
    print(f'Duration : {time.perf_counter() - start_time}')

    return True


def other_main():
    start_time = time.perf_counter()
    tasks_to_do = []
    with open('1hr_run.csv', 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            tasks_to_do.append(row[1])
    while tasks_to_do:
        puzzle = Puzzle()
        puzzle.build_from_string(tasks_to_do.pop())
        solution = brute_force(puzzle)
        print(f'{len(tasks_to_do)} tasks remaining')
        
    print(f'duration: {time.perf_counter() - start_time}')


if __name__ == '__main__':
    main()
