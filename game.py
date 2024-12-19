import tkinter as tk
from gameAI import get_ai_move

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.attributes('-fullscreen', True)

        self.current_player = "X"
        self.board = [[None for _ in range(3)] for _ in range(3)]

        self.timer_label = tk.Label(self.window, text="Time left: 2", font=("Arial", 24))
        self.timer_label.pack()

        self.info_label = tk.Label(self.window, text="Player X's Turn", font=("Arial", 24))
        self.info_label.pack()

        self.time_left = 2
        self.timer_running = False
        self.timer_id = None

        self.create_board()
        self.create_controls()

    def create_board(self):
        self.canvas = tk.Canvas(self.window, width=600, height=600, bg="white")
        self.canvas.pack(expand=True)

        # Draw grid lines
        for i in range(1, 3):
            self.canvas.create_line(0, i * 200, 600, i * 200, width=4)
            self.canvas.create_line(i * 200, 0, i * 200, 600, width=4)

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.start_timer()

    def create_controls(self):
        controls_frame = tk.Frame(self.window)
        controls_frame.pack()

        reset_button = tk.Button(controls_frame, text="Restart Game", font=("Arial", 20), command=self.reset_game)
        reset_button.pack(side=tk.LEFT, padx=10)

        quit_button = tk.Button(controls_frame, text="Quit Game", font=("Arial", 20), command=self.window.destroy)
        quit_button.pack(side=tk.RIGHT, padx=10)

    def start_timer(self):
        self.time_left = 2
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
            self.switch_turn_due_to_timeout()

    def switch_turn_due_to_timeout(self):
        self.info_label.config(text=f"Player {self.current_player} ran out of time! Switching turns.")
        self.current_player = "O" if self.current_player == "X" else "X"
        self.info_label.config(text=f"Player {self.current_player}'s Turn")
        if self.current_player == "O":
            self.ai_move()
        else:
            self.start_timer()

    def on_canvas_click(self, event):
        if not self.timer_running or self.current_player != "X":
            return

        row, col = event.y // 200, event.x // 200
        if self.board[row][col] is None:
            self.board[row][col] = self.current_player
            self.draw_move(row, col)

            if self.check_winner():
                self.stop_timer()
                self.draw_winner_line()
                self.info_label.config(text=f"Player {self.current_player} wins!")
            elif self.is_draw():
                self.stop_timer()
                self.info_label.config(text="It's a draw!")
            else:
                self.current_player = "O"
                self.info_label.config(text=f"Player {self.current_player}'s Turn")
                self.ai_move()

    def ai_move(self):
        row, col = get_ai_move(self.board)
        self.board[row][col] = "O"
        self.draw_move(row, col)

        if self.check_winner():
            self.stop_timer()
            self.draw_winner_line()
            self.info_label.config(text=f"Player {self.current_player} wins!")
        elif self.is_draw():
            self.stop_timer()
            self.info_label.config(text="It's a draw!")
        else:
            self.current_player = "X"
            self.info_label.config(text=f"Player {self.current_player}'s Turn")
            self.start_timer()

    def stop_timer(self):
        if self.timer_id is not None:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None

    def draw_move(self, row, col):
        x1, y1 = col * 200 + 20, row * 200 + 20
        x2, y2 = (col + 1) * 200 - 20, (row + 1) * 200 - 20

        if self.current_player == "X":
            self.canvas.create_line(x1, y1, x2, y2, width=4, fill="blue")
            self.canvas.create_line(x1, y2, x2, y1, width=4, fill="blue")
        else:
            self.canvas.create_oval(x1, y1, x2, y2, width=4, outline="red")

    def draw_winner_line(self):
        # Check rows and columns for a winner
        for i in range(3):
            if all(self.board[i][j] == self.current_player for j in range(3)):
                self.canvas.create_line(20, i * 200 + 100, 580, i * 200 + 100, width=4, fill="green")
                return
            if all(self.board[j][i] == self.current_player for j in range(3)):
                self.canvas.create_line(i * 200 + 100, 20, i * 200 + 100, 580, width=4, fill="green")
                return

        # Check diagonals for a winner
        if all(self.board[i][i] == self.current_player for i in range(3)):
            self.canvas.create_line(20, 20, 580, 580, width=4, fill="green")
            return
        if all(self.board[i][2 - i] == self.current_player for i in range(3)):
            self.canvas.create_line(20, 580, 580, 20, width=4, fill="green")

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
        self.stop_timer()
        self.current_player = "X"
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.canvas.delete("all")

        # Redraw grid lines
        for i in range(1, 3):
            self.canvas.create_line(0, i * 200, 600, i * 200, width=4)
            self.canvas.create_line(i * 200, 0, i * 200, 600, width=4)

        self.info_label.config(text=f"Player {self.current_player}'s Turn")
        self.start_timer()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
