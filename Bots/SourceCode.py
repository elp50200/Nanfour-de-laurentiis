# the connect4 class that will be used to judge your code
class Connect4:
    def __init__(self):
        self.board = [[0] * 7 for _ in range(6)]
        self.turn = 1 # player 1 goes first

    def detect_win(self):
        dirs = [(0,1), (1,0), (1,1), (1,-1)]
        rows, cols = 6, 7
        for x in range(rows):
            for y in range(cols):
                if self.board[x][y] != 0:
                    for dx, dy in dirs:
                        if all(0 <= x+i*dx < rows and 0 <= y+i*dy < cols and
                               self.board[x+i*dx][y+i*dy] == self.board[x][y] for i in range(4)):
                            return self.board[x][y]
        return 0

    def make_move(self, col):
        if col < 0 or col > 6:
            return False
        for row in range(6):
            if self.board[row][col] == 0:
                self.board[row][col] = self.turn
                self.turn = 3 - self.turn
                return True
        return False