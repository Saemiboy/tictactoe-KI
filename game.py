import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")

        self.current_player = "X"
        self.board = [[None for _ in range(3)] for _ in range(3)]

        self.create_board()

    def create_board(self):
        self.canvas = tk.Canvas(self.window, width=300, height=300, bg="white")
        self.canvas.pack()

        # Draw grid lines
        for i in range(1, 3):
            self.canvas.create_line(0, i * 100, 300, i * 100, width=2)
            self.canvas.create_line(i * 100, 0, i * 100, 300, width=2)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        row, col = event.y // 100, event.x // 100
        if self.board[row][col] is None:
            self.board[row][col] = self.current_player
            self.draw_move(row, col)

            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def draw_move(self, row, col):
        x1, y1 = col * 100 + 20, row * 100 + 20
        x2, y2 = (col + 1) * 100 - 20, (row + 1) * 100 - 20

        if self.current_player == "X":
            self.canvas.create_line(x1, y1, x2, y2, width=4, fill="blue")
            self.canvas.create_line(x1, y2, x2, y1, width=4, fill="blue")
        else:
            self.canvas.create_oval(x1, y1, x2, y2, width=4, outline="red")

    def check_winner(self):
        # Check rows and columns
        for i in range(3):
            if all(self.board[i][j] == self.current_player for j in range(3)) or \
               all(self.board[j][i] == self.current_player for j in range(3)):
                return True

        # Check diagonals
        if all(self.board[i][i] == self.current_player for i in range(3)) or \
           all(self.board[i][2 - i] == self.current_player for i in range(3)):
            return True

        return False

    def is_draw(self):
        return all(self.board[row][col] is not None for row in range(3) for col in range(3))

    def reset_game(self):
        self.current_player = "X"
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.canvas.delete("all")

        # Redraw grid lines
        for i in range(1, 3):
            self.canvas.create_line(0, i * 100, 300, i * 100, width=2)
            self.canvas.create_line(i * 100, 0, i * 100, 300, width=2)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
