import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")

        self.current_player = "X"
        self.board = [[None for _ in range(3)] for _ in range(3)]

        self.create_buttons()

    def create_buttons(self):
        self.buttons = []
        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(self.window, text="", font=("Arial", 24), height=2, width=5,
                                   command=lambda r=row, c=col: self.on_button_click(r, c))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    def on_button_click(self, row, col):
        if self.board[row][col] is None:
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, state=tk.DISABLED)

            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

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
        for row in self.buttons:
            for button in row:
                button.config(text="", state=tk.NORMAL)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
