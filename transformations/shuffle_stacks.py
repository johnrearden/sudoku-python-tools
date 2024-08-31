import numpy as np


def shuffle_stacks(puzzle_string):
    puzzle_array = np.array(
        [0 if char == '-' else int(char) for char in puzzle_string]
    )
    puzzle_array = puzzle_array.reshape((9, 9))

    # Set up stacks
    stack_array = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
    stack_array = np.reshape(stack_array, (3, 3))
    from_arr = stack_array.flatten()
    permuted_array = np.random.permutation(stack_array)
    to_arr = permuted_array.flatten()

    # Swap the stacks
    for i in range(0, 9):
        f = from_arr[i]
        t = to_arr[i]
        puzzle_array[:, [f, t]] = puzzle_array[:, [t, f]]

    new_string = ''.join(
        ['-' if n == 0 else str(n) for n in puzzle_array.flatten()]
    )
    return new_string
