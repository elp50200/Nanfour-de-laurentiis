import numpy as np
from Bots.VAMPIRE import Player as VampirePlayer
from Bots.guillermo import Player as GuillermoPlayer

def print_board(board):
    print(np.flip(board, 0))

def play_game():
    board = np.zeros((6, 7), dtype=int)
    game_over = False
    turn = 0
    play = 0

    player1 = VampirePlayer(playerOne=True)  # Player 1 using VAMPIRE
    player2 = GuillermoPlayer(playerOne=False)  # Player 2 using guillermo

    while not game_over:
        if turn == 0:
            col = player1.makeMove(board)
            if player1.is_valid_location(board, col):
                print("Player 1 (VAMPIRE) chose column", col)
                row = player1.get_next_open_row(board, col)
                player1.drop_piece(board, row, col, player1.player)
                if player1.detect_win(board, player1.player):
                    print("Player 1 (VAMPIRE) wins!")
                    game_over = True
        else:
            col = player2.makeMove(board)
            if player2.is_valid_location(board, col):
                print("Player 2 (guillermo) chose column", col)
                row = player2.get_next_open_row(board, col)
                player2.drop_piece(board, row, col, player2.player)
                if player2.detect_win(board, player2.player):
                    print("Player 2 (guillermo) wins!")
                    game_over = True

        play += 1
        print_board(board)
        print(play)
        print("\n")

        turn += 1
        turn = turn % 2

        if len(player1.get_valid_locations(board)) == 0:
            print("Game is a draw!")
            game_over = True

if __name__ == "__main__":
    play_game()