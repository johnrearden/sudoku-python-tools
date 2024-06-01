import threading
from tools.classes import Puzzle
from tools.utils import check_puzzle_validity
from tools.sudoku_gui import CombinedSudokuGUI
from solving_strategies.one_per_nonet import one_per_nonet

import time
import queue
import os


def main():
    puzzle_string_1 = (
        '''------6-91----4-----53-6821--467--5---7---9-----54----37-4-52-6-'''
        '''-----51--6--2--37'''
    )
    puzzle_string_2 = (
        '''25------4----5---9-8-3--25---------2-3---7---8---4-16-1---6-58--'''
        '''------9---64-----'''
    )
    puzzle = Puzzle()
    puzzle.build_from_string(puzzle_string_1)
    
    update_queue = queue.Queue()
    
    gui_thread = threading.Thread(
        target=run_gui,
        args=(puzzle.cells, puzzle.notes, update_queue))
    gui_thread.daemon = True
    gui_thread.start()

    while True:
        puzzle_changed = one_per_nonet(puzzle)
        #os.system('clear')
        print(puzzle)
        update_queue.put((puzzle.cells, puzzle.notes))
        time.sleep(1)
        if not puzzle_changed:
            break

    gui_thread.join()


def run_gui(sudoku, notes, update_queue):
    gui = CombinedSudokuGUI(sudoku, notes, update_queue)
    gui.run()


if __name__ == '__main__':
    main()