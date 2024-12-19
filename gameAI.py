import random

def get_ai_move(board):
    """
    Returns the best move for the AI (Player O) using a simple algorithm.
    :param board: The current game board as a 2D list.
    :return: (row, col) tuple for the AI's move.
    """
    # Check if AI can win in the next move
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = "O"
                if check_winner(board, "O"):
                    return i, j
                board[i][j] = None

    # Block player's winning move
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = "X"
                if check_winner(board, "X"):
                    board[i][j] = None
                    return i, j
                board[i][j] = None

    # Take center if available
    if board[1][1] is None:
        return 1, 1

    # Take a random corner if available
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    random.shuffle(corners)
    for row, col in corners:
        if board[row][col] is None:
            return row, col

    # Take a random side if available
    sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
    random.shuffle(sides)
    for row, col in sides:
        if board[row][col] is None:
            return row, col

    # If no other move is possible (should not happen in a valid game)
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                return i, j


def check_winner(board, player):
    """
    Checks if the given player has won the game.
    :param board: The current game board as a 2D list.
    :param player: "X" or "O".
    :return: True if the player has won, False otherwise.
    """
    # Check rows and columns
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
           all(board[j][i] == player for j in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2 - i] == player for i in range(3)):
        return True

    return False
