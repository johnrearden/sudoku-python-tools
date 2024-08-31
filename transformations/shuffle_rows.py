import numpy as np


def shuffle_rows(puzzle_string):
    puzzle_array = np.array(
        [0 if char == '-' else int(char) for char in puzzle_string]
    )
    puzzle_array = puzzle_array.reshape((9, 9))

    to_array = np.concatenate((
        np.random.permutation(np.array([0, 1, 2])),
        np.random.permutation(np.array([3, 4, 5])),
        np.random.permutation(np.array([6, 7, 8])),
    ))

    swapped_array = np.zeros([9, 9], dtype=int)

    # Swap the rows
    for i in range(0, 9):
        t = to_array[i]
        swapped_array[:, [i]] = puzzle_array[:, [t]]

    new_string = ''.join(
        ['-' if n == 0 else str(n) for n in swapped_array.flatten()]
    )

    return new_string
