from tools.classes import Puzzle
from tools.utils import check_puzzle_validity
from solving_strategies.one_per_nonet import one_per_nonet


def main():
    puzzle_string = (
        '''------6-91----4-----53-6821--467--5---7---9-----54----37-4-52-6-'''
        '''-----51--6--2--37'''
    )
    puzzle = Puzzle()
    puzzle.build_from_string(puzzle_string)
        
    print(puzzle)
    one_per_nonet(puzzle)

    


if __name__ == '__main__':
    main()