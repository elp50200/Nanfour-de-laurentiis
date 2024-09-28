# Fill in the makeMove function
class Player:

	def __init__(self, playerOne):
		if playerOne is True:
			self.player = 1
			self.oppo = 2
		else:
			self.player = 2
			self.oppo = 1


	def makeMove(self, gameState) -> int:
		for col in range(6):
			if self.validMove(gameState, col):
				return col
		return 6


	def validMove(self, gameState, col):
		if col < 0 or col > 6:
			return False
		for row in range(6):
			if gameState[row][col] == 0:
				return True
		return False