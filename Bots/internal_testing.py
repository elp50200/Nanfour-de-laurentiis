import colin
import laslo
import nadja
import VAMPIRE
import SourceCode

game = SourceCode.Connect4()

#model = colin.Player(playerOne=True)
#model = colin.Player(playerOne=False)
#model = laslo.Player(playerOne=True)
#model = laslo.Player(playerOne=False)
#model = nadja.Player(playerOne=True)
#model = nadja.Player(playerOne=False)
player1 = VAMPIRE.Player(playerOne=True)
player2 = VAMPIRE.Player(playerOne=False)

while True:
    if game.turn == 1:
        game.make_move(player1.makeMove(game.board))
    else:
        game.make_move(player2.makeMove(game.board))

    if game.detect_win():
        if game.turn == 1:
            print("Player 2 Wins")
        else:
            print("Player 1 Wins")
        break


