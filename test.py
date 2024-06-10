import threading
from tools.classes import Puzzle
from tools.utils import (
    check_puzzle_validity, recalculate_notes, puzzle_complete,
    get_puzzle_cells_as_string
)
from tools.sudoku_gui import CombinedSudokuGUI
from tools.constants import SolverResult
from tools.uniqueness_test import is_unique

from solving_strategies.one_per_nonet import one_per_nonet
from solving_strategies.hidden_single import hidden_single
from solving_strategies.naked_pairs import naked_pairs
from solving_strategies.naked_triples import naked_triples
from solving_strategies.hidden_pairs import hidden_pairs
from solving_strategies.hidden_triples import hidden_triples
from solving_strategies.brute_force import brute_force
from solving_strategies.naked_quads import naked_quads
from solving_strategies.x_wing import x_wing_rows
from solving_strategies.x_wing import x_wing_cols
from solving_strategies.locked_candidates import locked_candidates_pointing
from solving_strategies.locked_candidates import locked_candidates_claiming

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
    
    puzzle_string_5 = ('''--7--6-1--4-----9-8---5-6-4'''
                       '''-1---57-2-------6---3-8----'''
                       '''-2---74-51--2-------------9''')
    
    puzzle_string_master = (
        '''-6----3--1-----4293--9-8---'''
        '''7----4--6--8-----54--15----'''
        '''-----9-1-64----25-----7-9--'''
    )
    
    puzzle_string_extreme = (
        '''--8-6------9---2-45--2-----'''
        '''-----5--1-----8-95---673---'''
        '''-------7-73----5---6-8---3-'''
    )
    
    puzzle_string_extreme2 = (
        '''6-----8----5----3----5-24--'''
        '''-8--43---716-------3---9---'''
        '''----7------8-1---6---3---71'''
    )
    puzzle_string_extreme3 = (
        '''--569-----3------9--8----1-'''
        '''47--3----1----4--8-----7---'''
        '''------471---2--3-----3-58--'''
    )
    
    solvers = [
        one_per_nonet,
        hidden_single,
        naked_pairs,
        naked_triples,
        hidden_pairs,
        hidden_triples,
        naked_quads,
        x_wing_rows,
        x_wing_cols,
        locked_candidates_pointing,
        locked_candidates_claiming,
    ]
    solver_usage = defaultdict(int)
    
    puzzle = Puzzle()
    puzzle.build_from_string(puzzle_string_extreme2)
    
    update_queue = queue.Queue()
    
    gui_thread = threading.Thread(
        target=run_gui,
        args=(puzzle.cells, puzzle.notes, update_queue))
    gui_thread.daemon = True
    gui_thread.start()

    while True:
        at_least_one_success = False
        puzzle_solved = False
        for _, solver in enumerate(solvers):
            puzzle_changed = solver(puzzle)
            if puzzle_changed != SolverResult.NO_CHANGE:
                print(f'{solver.__name__} successful')
                at_least_one_success = True
                solver_usage[solver.__name__] += 1
                update_queue.put((puzzle.cells, puzzle.notes))
                if puzzle_complete(puzzle):
                    puzzle_solved = True
            else:
                print(f'{solver.__name__} no results')
        if not at_least_one_success:
            print('------------------------------')
            print('no solution with these solvers')
            break
        if puzzle_solved:
            print('Puzzle is solved!')
            print(solver_usage)
            break

    print('Out of while loop')
    #brute_force(puzzle)
    #update_queue.put((puzzle.cells, puzzle.notes))
    time.sleep(.1)

    gui_thread.join()


def run_gui(sudoku, notes, update_queue):
    gui = CombinedSudokuGUI(sudoku, notes, update_queue)
    gui.run()
    
    
def test_brute_force():
    puzzle_string_4 = ('''-4--2-8--21---------9--45--'''
                       '''--7--96----43---8----------'''
                       '''--8--6-7------2-1-7-1-9--3-'''
                       )
    puzzle_string_1 = (
        '''------6-91----4-----53-6821--467--5---7---9-----54----37-4-52-6-'''
        '''-----51--6--2--37'''
    )
    puzzle_string_2 = (
        '''25------4----5---9-8-3--25---------2-3---7---8---4-16-1---6-58--'''
        '''------9---64-----'''
    )
    puzzle_string_60 = (
        '''538764219162--873-4791326--'''
        '''3---7--2-72-34--51---25-47-'''
        '''-13-2756-6-7-1----25-68-1-7'''
    )
    # These are examples of puzzle strings that represent Sudoku puzzles. Each
    # digit in the string represents a cell in the Sudoku grid. The hyphens
    # represent empty cells that need to be filled in. The numbers and hyphens
    # are arranged in a specific pattern to create a unique puzzle that can be
    # solved using the Sudoku solving strategies implemented in the code.
    puzzle_string_38 = (
        '''-387642--16---8-3-4791-26--'''
        '''3------2--2-34--51---25-4--'''
        '''-13-275--6-7-1----25-6----7'''
    )
    puzzle_string_35 = (
        '''25------4----5---9-8-3--257'''
        '''--------2-3---79488---4-165'''
        '''1---6-583--8---496--64--721'''
    )
    puzzle_string_extreme2 = (
        '''6-----8----5----3----5-24--'''
        '''-8--43---716-------3---9---'''
        '''----7------8-1---6---3---71'''
    )
    
    puzzle_string_extreme3 = (
        '''--569-----3------9--8----1-'''
        '''47--3----1----4--8-----7---'''
        '''------471---2--3-----3-58--'''
    )
    
    puzzle_string_generated = '--3-5-2146---8--3----1-3-875-----14----2-5--------9--2--48----5--26---7---7-2---3'
    start_time = time.perf_counter()
    
    puzzle = Puzzle()
    puzzle.build_from_string(puzzle_string_generated)
    print(get_puzzle_cells_as_string(puzzle))
    # for i in range(81):
    #     if puzzle.cells[i] == 1 or puzzle.cells[i] == 2:
    #         puzzle.cells[i] = 0
    # print(get_puzzle_cells_as_string(puzzle))
    result = brute_force(puzzle)
    print('result:', result)
    print(f'time taken: {time.perf_counter() - start_time:0.3f}')


if __name__ == '__main__':
    # main()
    test_brute_force()