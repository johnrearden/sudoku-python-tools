import numpy as np
from tools.constants import nonets, nonets_for_cell


class NpPuzzle:
    def __init__(self):
        self.cells = np.zeros(81, dtype=np.int8)
        self.notes = np.zeros((81, 9), dtype=bool)

    def build_from_string(self, str):
        for idx, char in enumerate(str):
            if char.isnumeric():
                self.cells[idx] = int(char)

    def calculate_notes(self, remove_only=True):
        for note_idx in range(81):
            if self.cells[note_idx] > 0:
                self.notes[note_idx] = np.zeros(9, dtype=bool)
                continue
            nonets_to_check = [nonets[n] for n in nonets_for_cell[note_idx]]
            results = np.ones((4, 9), dtype=bool)
            if remove_only:
                results[3] = self.notes[note_idx]  # 'and' with original notes
            else:
                results[3] = np.ones(9, dtype=bool)  # No effect on 'and'
            for idx, nonet in enumerate(nonets_to_check):
                result = np.ones(9, dtype=bool)
                for cell_idx in nonet:
                    value = self.cells[cell_idx]
                    if value > 0 or note_idx == cell_idx:
                        result[value - 1] = False
                results[idx] = result
            self.notes[note_idx] = np.logical_and.reduce(results)

    def calculate_notes_for_cell(self, index):
        if self.cells[index] > 0:
            self.notes[index] = np.zeros(9, dtype=bool)
            return
        nonets_to_check = [nonets[n] for n in nonets_for_cell[index]]
        results = np.ones((3, 9), dtype=bool)

        for idx, nonet in enumerate(nonets_to_check):
            result = np.ones(9, dtype=bool)
            for cell_idx in nonet:
                value = self.cells[cell_idx]
                if value > 0:
                    result[value - 1] = False

            results[idx] = result
        self.notes[index] = np.logical_and.reduce(
            [results[0], results[1], results[2]])

        cell_value = self.cells[index]
        if cell_value > 0:
            self.notes[index][cell_value - 1] = False

    def check_cell_is_valid(self, cell_idx):
        """
        Returns boolean indicating whether the current value of the cell at
        the index supplied as an argument is valid given the current state of
        the grid. Returns True if the value in the cell is empty (zero)
        """
        if self.cells[cell_idx] == 0:
            print('value is 0')
            return True
        value = self.cells[cell_idx]
        nonet_indices = nonets_for_cell[cell_idx]
        check_nonets = [nonets[n] for n in nonet_indices]
        for nonet in check_nonets:
            for idx in nonet:
                if idx != cell_idx and self.cells[idx] == value:
                    return False
        return True
    
    def get_known_cells_count(self):
        return sum(1 for cell in self.cells if cell > 0)

    def clone(self):
        clone = NpPuzzle()
        clone.cells = np.copy(self.cells)
        clone.notes = np.copy(self.notes)
        return clone

    def __str__(self):
        return ''.join([str(n) if n > 0 else '-' for n in self.cells])


class Puzzle:

    def __init__(self):
        self.cells = []
        self.notes = []
        self.known_cells_count = 0
        notes = [n for n in range(1, 10)]
        for _ in range(81):
            self.cells.append(0)
            self.notes.append(notes[:])

    def build_from_string(self, str):
        for index, char in enumerate(str):
            try:
                self.cells[index] = int(char)
                self.notes[index] = [int(char)]
            except ValueError:
                self.cells[index] = 0

    def remaining_cells(self):
        counter = 0
        for cell in self.cells:
            if cell == 0:
                counter += 1
        return counter

    def knowns_count(self):
        return 81 - self.remaining_cells()

    def clone(self):
        clone = Puzzle()
        clone.cells = self.cells[:]
        clone.notes = []
        for notes in self.notes:
            clone.notes.append(notes[:])
        assert clone.cells == self.cells
        assert clone.notes == self.notes
        return clone
    
    def get_known_cells_count(self):
        known_cells = [self.cells[n] for n in range(81) if self.cells[n] != 0]
        return len(known_cells)
    
    def to_short_string(self):
        return ''.join([str(n) if n > 0 else '-' for n in self.cells])

    def __str__(self):
        horizontal_line = '-------------------------------------\n'
        output = []
        output.append(horizontal_line)
        for i in range(0, 81, 9):
            strings = [str(n) for n in self.cells[i: i + 9]]
            line = '| ' + ' | '.join(strings) + ' |' + '\n'
            line = line.replace('0', ' ')
            output.append(line)
            output.append(horizontal_line)
        result = ''.join(output)
        
        remaining_cells = str(self.remaining_cells())    

        return f'{result}\nCells Remaining: {remaining_cells}'
