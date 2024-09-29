import numpy as np
from Bots.VAMPIRE import Player as VampirePlayer
from Bots.guillermo import Player as GuillermoPlayer
from Bots.werewolf import Player as WerewolfPlayer

def print_board(board):
    print(np.flip(board, 0))

def is_valid_location(board, col):
    return board[5][col] == 0

def get_next_open_row(board, col):
    for r in range(6):
        if board[r][col] == 0:
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def detect_win(board, piece):
    # Check horizontal locations
    for c in range(7 - 3):
        for r in range(6):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True
    # Check vertical locations
    for c in range(7):
        for r in range(6 - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True
    # Check positively sloped diagonals
    for c in range(7 - 3):
        for r in range(6 - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True
    # Check negatively sloped diagonals
    for c in range(7 - 3):
        for r in range(3, 6):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True
    return False

def get_valid_locations(board):
    valid_locations = []
    for col in range(7):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def play_game():
    board = np.zeros((6, 7), dtype=int)
    game_over = False
    turn = 0
    play = 0

    player1 = WerewolfPlayer(playerOne=True)  # Player 1 using VAMPIRE
    player2 = WerewolfPlayer(playerOne=False)  # Player 2 using guillermo

    while not game_over:
        if turn == 0:
            col = player1.makeMove(board)
            if is_valid_location(board, col):
                print("Player 1 (VAMPIRE) chose column", col)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, player1.player)
                if detect_win(board, player1.player):
                    print("Player 1 (VAMPIRE) wins!")
                    game_over = True
        else:
            col = player2.makeMove(board)
            if is_valid_location(board, col):
                print("Player 2 (guillermo) chose column", col)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, player2.player)
                if detect_win(board, player2.player):
                    print("Player 2 (guillermo) wins!")
                    game_over = True

        play += 1
        print_board(board)
        print(play)
        print("\n")

        turn += 1
        turn = turn % 2

        if len(get_valid_locations(board)) == 0:
            print("Game is a draw!")
            game_over = True

if __name__ == "__main__":
    play_game()