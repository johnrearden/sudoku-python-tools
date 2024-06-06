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
