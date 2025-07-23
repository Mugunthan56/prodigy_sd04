import tkinter as tk
from tkinter import messagebox

class SudokuSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🧩 Sudoku Solver")
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.user_inputs = set()
        self.status_label = tk.Label(root, text="", font=("Arial", 14), fg="green")
        self.status_label.grid(row=10, column=0, columnspan=9, pady=5)

        # Register input validation
        vcmd = (self.root.register(self.validate_input), '%P')

        self.create_grid(vcmd)

        tk.Button(root, text="Solve", command=self.solve).grid(row=9, column=0, columnspan=4, sticky="we", pady=5)
        tk.Button(root, text="Reset", command=self.reset_board).grid(row=9, column=5, columnspan=4, sticky="we", pady=5)

    def validate_input(self, new_value):
        # Allow only empty or 1-9
        if new_value == "":
            return True
        return new_value.isdigit() and 1 <= int(new_value) <= 9

    def create_grid(self, vcmd):
        for i in range(9):
            for j in range(9):
                e = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center',
                             validate="key", validatecommand=vcmd)
                e.grid(row=i, column=j, padx=3, pady=3)
                self.cells[i][j] = e

    def get_board(self):
        board = []
        self.user_inputs.clear()
        for i in range(9):
            row = []
            for j in range(9):
                val = self.cells[i][j].get().strip()
                if val.isdigit() and 1 <= int(val) <= 9:
                    row.append(int(val))
                    self.user_inputs.add((i, j))
                else:
                    row.append(0)
            while len(row) < 9:
                row.append(0)
            board.append(row)
        return board

    def highlight_errors(self, board):
        error_cells = self.find_duplicates(board)
        for i in range(9):
            for j in range(9):
                if (i, j) in error_cells:
                    self.cells[i][j].config(fg='red')
                elif (i, j) in self.user_inputs:
                    self.cells[i][j].config(fg='blue')
                else:
                    self.cells[i][j].config(fg='black')
        return len(error_cells) == 0

    def find_duplicates(self, board):
        errors = set()

        # Row check
        for i in range(9):
            seen = {}
            for j in range(9):
                val = board[i][j]
                if val != 0:
                    if val in seen:
                        errors.add((i, j))
                        errors.add((i, seen[val]))
                    else:
                        seen[val] = j

        # Column check
        for j in range(9):
            seen = {}
            for i in range(9):
                val = board[i][j]
                if val != 0:
                    if val in seen:
                        errors.add((i, j))
                        errors.add((seen[val], j))
                    else:
                        seen[val] = i

        # Box check
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                seen = {}
                for i in range(3):
                    for j in range(3):
                        row = box_row + i
                        col = box_col + j
                        val = board[row][col]
                        if val != 0:
                            if val in seen:
                                errors.add((row, col))
                                errors.add(seen[val])
                            else:
                                seen[val] = (row, col)

        return errors

    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                self.cells[i][j].insert(0, str(board[i][j]))
                if (i, j) in self.user_inputs:
                    self.cells[i][j].config(fg='blue')
                else:
                    self.cells[i][j].config(fg='black')

    def solve(self):
        board = self.get_board()
        if not self.highlight_errors(board):
            self.status_label.config(text="❌ Invalid input: Repeated numbers!", fg="red")
            return
        if self.solve_sudoku(board):
            self.set_board(board)
            self.status_label.config(text="✅ Sudoku Solved Successfully!", fg="green")
        else:
            self.status_label.config(text="❌ No solution found!", fg="red")

    def reset_board(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                self.cells[i][j].config(fg='black')
        self.status_label.config(text="")
        self.user_inputs.clear()

    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def is_safe(self, board, row, col, num):
        if num in board[row]: return False
        if num in [board[i][col] for i in range(9)]: return False
        box_row, box_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                if board[box_row+i][box_col+j] == num:
                    return False
        return True

    def solve_sudoku(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True
        row, col = empty
        for num in range(1, 10):
            if self.is_safe(board, row, col, num):
                board[row][col] = num
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverGUI(root)
    root.mainloop()
