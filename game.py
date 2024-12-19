import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")

        self.current_player = "X"
        self.board = [[None for _ in range(3)] for _ in range(3)]

        self.timer_label = tk.Label(self.window, text="Time left: 10", font=("Arial", 14))
        self.timer_label.pack()

        self.time_left = 3
        self.timer_running = False
        self.timer_id = None

        self.create_board()

    def create_board(self):
        self.canvas = tk.Canvas(self.window, width=300, height=300, bg="white")
        self.canvas.pack()

        # Draw grid lines
        for i in range(1, 3):
            self.canvas.create_line(0, i * 100, 300, i * 100, width=2)
            self.canvas.create_line(i * 100, 0, i * 100, 300, width=2)

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.start_timer()

    def start_timer(self):
        self.time_left = 10
        if self.timer_id is not None:
            self.window.after_cancel(self.timer_id)
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.timer_running = True
            self.timer_label.config(text=f"Time left: {self.time_left}")
            self.time_left -= 1
            self.timer_id = self.window.after(1000, self.update_timer)
        else:
            self.timer_running = False
            messagebox.showinfo("Time Out", f"Player {self.current_player} ran out of time! Switching turns.")
            self.current_player = "O" if self.current_player == "X" else "X"
            self.start_timer()

    def on_canvas_click(self, event):
        if not self.timer_running:
            return

        row, col = event.y // 100, event.x // 100
        if self.board[row][col] is None:
            self.board[row][col] = self.current_player
            self.draw_move(row, col)

            if self.check_winner():
                self.draw_winner_line()
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.start_timer()

    def draw_move(self, row, col):
        x1, y1 = col * 100 + 20, row * 100 + 20
        x2, y2 = (col + 1) * 100 - 20, (row + 1) * 100 - 20

        if self.current_player == "X":
            self.canvas.create_line(x1, y1, x2, y2, width=4, fill="blue")
            self.canvas.create_line(x1, y2, x2, y1, width=4, fill="blue")
        else:
            self.canvas.create_oval(x1, y1, x2, y2, width=4, outline="red")

    def draw_winner_line(self):
        # Check rows and columns for a winner
        for i in range(3):
            if all(self.board[i][j] == self.current_player for j in range(3)):
                self.canvas.create_line(10, i * 100 + 50, 290, i * 100 + 50, width=4, fill="green")
                return
            if all(self.board[j][i] == self.current_player for j in range(3)):
                self.canvas.create_line(i * 100 + 50, 10, i * 100 + 50, 290, width=4, fill="green")
                return

        # Check diagonals for a winner
        if all(self.board[i][i] == self.current_player for i in range(3)):
            self.canvas.create_line(10, 10, 290, 290, width=4, fill="green")
            return
        if all(self.board[i][2 - i] == self.current_player for i in range(3)):
            self.canvas.create_line(10, 290, 290, 10, width=4, fill="green")

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

        self.start_timer()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
