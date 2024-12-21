import pytest
from solving_strategies.brute_force import brute_force
from tools.utils import check_puzzle_validity
from tools.classes import Puzzle

class TestBruteForceSolver:
    @pytest.fixture
    def easy_valid_puzzle(self):
        puzzle = Puzzle()
        puzzle.build_from_string(
            '8-679-4--34--1-792-7--53----2--845-----239--4--8---6--591-----7-----7--6-6-92-38-'
        )
        return puzzle

    def test_easy_puzzle(self, easy_valid_puzzle):
        puzzle = easy_valid_puzzle
        solved_puzzle = brute_force(puzzle)
        assert check_puzzle_validity(solved_puzzle)
