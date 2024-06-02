import tkinter as tk
import queue


class SudokuGUI:
    def __init__(self, parent, sudoku):
        self.root = parent
        self.cells = []
        self.note_cells = []

        self.create_grid()
        self.update_puzzle(sudoku)

    def create_grid(self):
        for i in range(9):
            row = []
            for j in range(9):
                cell = tk.Entry(
                    self.root, width=2, font=('Arial', 25), justify='center')
                cell.grid(row=i, column=j)
                if (i // 3 + j // 3) % 2 == 0:
                    cell.configure(bg="lightgrey")
                row.append(cell)
            self.cells.append(row)

    def update_puzzle(self, sudoku):
        for i in range(9):
            for j in range(9):
                cell_value = sudoku[i * 9 + j]
                cell_text = str(cell_value) if cell_value != 0 else ''
                self.cells[i][j].delete(0, tk.END)
                self.cells[i][j].insert(tk.END, cell_text)


class SudokuNotesGUI:
    def __init__(self, parent, notes, sudoku):
        self.notes = notes
        self.root = parent
        self.cells = []
        self.create_grid()
        self.update_notes(self.notes, sudoku)

    def create_grid(self):
        for i in range(9):
            row = []
            for j in range(9):
                frame = tk.Frame(self.root, borderwidth=1, relief="solid")
                frame.grid(row=i, column=j, padx=1, pady=1)
                sub_cells = []
                for k in range(3):
                    sub_row = []
                    for l in range(3):
                        cell = tk.Label(frame, text="", width=2, height=1, font=('Arial', 10))
                        cell.grid(row=k, column=l)
                        if (i // 3 + j // 3) % 2 == 0:
                            cell.configure(bg="lightgrey")
                        else:
                            cell.configure(bg="white")
                        sub_row.append(cell)
                    sub_cells.append(sub_row)
                row.append(sub_cells)
            self.cells.append(row)
            
    def update_notes(self, notes, sudoku):
        for idx, note in enumerate(notes):
            row, col = divmod(idx, 9)
            for k in range(3):
                for l in range(3):
                    num = k * 3 + l + 1
                    if num in note and sudoku[idx] != num:
                        cell_text = str(num)
                    else:
                        cell_text = ""
                    #cell_text = str(num) if num in note else ""
                    self.cells[row][col][k][l].config(text=cell_text)


class CombinedSudokuGUI:
    def __init__(self, sudoku, notes, update_queue):
        self.root = tk.Tk()
        self.root.title("Sudoku with Notes")

        self.update_queue = update_queue

        self.sudoku_frame = tk.Frame(self.root)
        self.sudoku_frame.grid(row=0, column=0, padx=10, pady=10)

        self.notes_frame = tk.Frame(self.root)
        self.notes_frame.grid(row=0, column=1, padx=10, pady=10)

        self.sudoku_gui = SudokuGUI(self.sudoku_frame, sudoku)
        self.notes_gui = SudokuNotesGUI(self.notes_frame, notes, sudoku)
        
        self.check_updates()

    def run(self):
        self.root.mainloop()

    def check_updates(self):
        try:
            new_sudoku = self.update_queue.get_nowait()
            self.sudoku_gui.update_puzzle(new_sudoku[0])
            self.notes_gui.update_notes(new_sudoku[1], new_sudoku[0])
            self.root.update_idletasks()
        except queue.Empty:
            pass
        self.root.after(100, self.check_updates)
