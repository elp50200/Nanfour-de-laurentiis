import colin
import laslo
import nadja


gameState = [
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 2, 0, 0, 0, 0],
  [0, 0, 1, 0, 0, 0, 0],
  [0, 0, 1, 0, 1, 1, 0],
  [0, 0, 2, 1, 2, 2, 2]
]

'''
gameState = [
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0]
]
'''

model = colin.Player(playerOne=True)
#model = colin.Player(playerOne=False)
#model = laslo.Player(playerOne=True)
#model = laslo.Player(playerOne=False)
model = nadja.Player(playerOne=True)
#model = nadja.Player(playerOne=False)

print(model.makeMove(gameState))