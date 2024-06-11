from tools.classes import NpPuzzle


if __name__ == '__main__':
    ps = '-95-482---2-----53-73-529--5------98---5--427-8269-3--3-8--95624--2-5-8--598-6--4'
    print(ps)
    puzzle = NpPuzzle()
    puzzle.build_from_string(ps)
    print(puzzle)
    puzzle.calculate_notes()
    print(puzzle.notes[:20])
