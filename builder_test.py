from tools.generators import naive_builder
from tools.classes import Puzzle
from solving_strategies.brute_force import brute_force
from collections import defaultdict


def main():
    nonets_for_cell = defaultdict(list)
    for i in range(81):
        nonets_for_cell[i].append(i // 9)
        nonets_for_cell[i].append(9 + (i % 9))
        nonets_for_cell[i].append(18 + (3 * (i // 27)) + ((i // 3) % 3))
        print(f'{nonets_for_cell[i]},')


if __name__ == '__main__':
    #naive_builder()
    #main()
    puzzle = Puzzle()
    brute_force(puzzle, randomize_digit_order=False, verbose=False)