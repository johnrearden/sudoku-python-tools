import threading
from tools.classes import Puzzle
from tools.utils import check_puzzle_validity
from tools.sudoku_gui import CombinedSudokuGUI
from solving_strategies.one_per_nonet import one_per_nonet
from solving_strategies.missing_from_only_one import missing_from_only_one
from solving_strategies.brute_force import brute_force

import time
import queue
import os

from collections import defaultdict


def testing_main():
    puzzle_string_1 = (
        '''------6-91----4-----53-6821--467--5---7---9-----54----37-4-52-6-'''
        '''-----51--6--2--37'''
    )
    puzzle_string_2 = (
        '''25------4----5---9-8-3--25---------2-3---7---8---4-16-1---6-58--'''
        '''------9---64-----'''
    )
    puzzle = Puzzle()
    puzzle.build_from_string(puzzle_string_2)
    print(puzzle)

    previous_puzzle_cells = brute_force(puzzle, randomize_digit_order=True)

    for _ in range(10):
        puzzle = Puzzle()
        puzzle.build_from_string(puzzle_string_2)
        solved_cells = brute_force(puzzle, randomize_digit_order=True)
        if solved_cells != previous_puzzle_cells:
            print('Different solutions exist!')
            break
        else:
            previous_puzzle_cells = solved_cells
    print('puzzle solution seems to be unique')


def main():
    puzzle_string_1 = (
        '''------6-91----4-----53-6821--467--5---7---9-----54----37-4-52-6-'''
        '''-----51--6--2--37'''
    )
    puzzle_string_2 = (
        '''25------4----5---9-8-3--25---------2-3---7---8---4-16-1---6-58--'''
        '''------9---64-----'''
    )
    
    solvers = [
        one_per_nonet,
        missing_from_only_one,
    ]
    solver_usage = defaultdict(int)
    
    puzzle = Puzzle()
    puzzle.build_from_string(puzzle_string_2)
    
    update_queue = queue.Queue()
    
    gui_thread = threading.Thread(
        target=run_gui,
        args=(puzzle.cells, puzzle.notes, update_queue))
    gui_thread.daemon = True
    gui_thread.start()

    while True:
        for idx, solver in enumerate(solvers):
            puzzle_changed = solver(puzzle)
            if puzzle_changed:
                print(f'{solver.__name__} successful')
                solver_usage[solver] += 1
            else:
                print(f'{solver.__name__} no results')
                if idx == len(solvers) - 1:
                    print('------------------------------')
                    print('no solution with these solvers')
                    solvers[0](puzzle)
                    break
        if not puzzle_changed:
            break
        
        #os.system('clear')
        #print(puzzle)
        update_queue.put((puzzle.cells, puzzle.notes))
        time.sleep(.1)
        

    gui_thread.join()


def run_gui(sudoku, notes, update_queue):
    gui = CombinedSudokuGUI(sudoku, notes, update_queue)
    gui.run()


if __name__ == '__main__':
    main()