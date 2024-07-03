from tools.constants import nonets, nonets_for_cell
import random


def substitute_digits(puzzle_string):
    originals = [str(n) for n in range(1, 10)]
    substitutes = originals[:]
    random.shuffle(substitutes)
    digit_map = {k: v for (k, v) in zip(originals, substitutes)}
    new_string = ''.join(
        ['-' if char == '-' else digit_map[char] for char in puzzle_string]
    )
    return new_string
