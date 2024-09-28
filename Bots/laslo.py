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
		if self.player == 1:
			return 0
		else:
			return 6