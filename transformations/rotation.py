import numpy as np


def rotate_puzzle_string(puzzle_string, n_90=1):
    puzzle_array = np.array(
        [0 if char == '-' else int(char) for char in puzzle_string]
    )
    puzzle_array = puzzle_array.reshape((9, 9))
    puzzle_array = np.rot90(puzzle_array, k=n_90, axes=(1, 0))
    new_string = ''.join(
        ['-' if n == 0 else str(n) for n in puzzle_array.flatten()]
    )
    return new_string
