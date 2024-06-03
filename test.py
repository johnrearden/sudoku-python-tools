import threading
from tools.classes import Puzzle
from tools.utils import check_puzzle_validity, recalculate_notes
from tools.sudoku_gui import CombinedSudokuGUI
from tools.constants import SolverResult
from solving_strategies.one_per_nonet import one_per_nonet
from solving_strategies.missing_from_only_one import missing_from_only_one
from solving_strategies.naked_pairs import naked_pairs
from solving_strategies.naked_triples import naked_triples
from solving_strategies.hidden_pairs import hidden_pairs
from solving_strategies.hidden_triples import hidden_triples
from solving_strategies.brute_force import brute_force

import time
import queue

from collections import defaultdict


def main():
    puzzle_string_1 = (
        '''------6-91----4-----53-6821--467--5---7---9-----54----37-4-52-6-'''
        '''-----51--6--2--37'''
    )
    puzzle_string_2 = (
        '''25------4----5---9-8-3--25---------2-3---7---8---4-16-1---6-58--'''
        '''------9---64-----'''
    )
    puzzle_string_3 = ('''---41-8---8---3-----4---156'''
                       '''--6---2--2--3----47-3----1-'''
                       '''----4----5-1-7--986----1---'''
                       )
    puzzle_string_4 = ('''-4--2-8--21---------9--45--'''
                       '''--7--96----43---8----------'''
                       '''--8--6-7------2-1-7-1-9--3-'''
                       )
    
    solvers = [
        one_per_nonet,
        missing_from_only_one,
        naked_pairs,
        naked_triples,
        hidden_pairs,
        hidden_triples,
    ]
    solver_usage = defaultdict(int)
    
    puzzle = Puzzle()
    puzzle.build_from_string(puzzle_string_4)
    
    update_queue = queue.Queue()
    
    gui_thread = threading.Thread(
        target=run_gui,
        args=(puzzle.cells, puzzle.notes, update_queue))
    gui_thread.daemon = True
    gui_thread.start()

    while True:
        at_least_one_success = False
        for idx, solver in enumerate(solvers):
            puzzle_changed = solver(puzzle)
            if puzzle_changed != SolverResult.NO_CHANGE:
                print(f'{solver.__name__} successful')
                at_least_one_success = True
                solver_usage[solver] += 1
                update_queue.put((puzzle.cells, puzzle.notes))
            else:
                print(f'{solver.__name__} no results')
        if not at_least_one_success:
            print('------------------------------')
            print('no solution with these solvers')
            break

    print('Out of while loop')
    brute_force(puzzle)
    update_queue.put((puzzle.cells, puzzle.notes))
    time.sleep(.1)

    gui_thread.join()


def run_gui(sudoku, notes, update_queue):
    gui = CombinedSudokuGUI(sudoku, notes, update_queue)
    gui.run()


if __name__ == '__main__':
    main()