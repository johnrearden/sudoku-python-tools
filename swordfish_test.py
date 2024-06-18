from tools.classes import Puzzle
from solving_strategies.swordfish import swordfish_rows
from tools.utils import recalculate_notes

if __name__ == '__main__':
    p_str = (
        '''16-543-7--786-14354358-76-1'''
        '''72-458-696--912-57---376--4'''
        '''-16-3--4-3---8--16--71645-3'''
    )
    p_str_2 = (
        '''1-85--2345--3-2178---8--569'''
        '''8--6-5793--59--4813----8652'''
        '''98-2-631-------8-----78-9--'''
    )
    puzzle = Puzzle()
    puzzle.build_from_string(p_str_2)
    puzzle = recalculate_notes(puzzle)
    
    swordfish_rows(puzzle)