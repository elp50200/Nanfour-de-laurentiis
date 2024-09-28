import numpy as np
from Bots.SourceCode import Connect4

class Player:
    def __init__(self, playerOne):
        if playerOne:
            self.player = 1
            self.oppo = 2
        else:
            self.player = 2
            self.oppo = 1
        self.pheromone = np.ones((6, 7))  # Initialize pheromone levels

    def makeMove(self, gameState) -> int:
        board = np.array(gameState)
        best_col = self.ant_colony_optimization(board)
        return best_col

    def ant_colony_optimization(self, board):
        num_ants = 10
        num_iterations = 100
        decay = 0.95
        alpha = 1.0
        beta = 1.0

        for _ in range(num_iterations):
            all_solutions = []
            for _ in range(num_ants):
                solution = self.construct_solution(board, alpha, beta)
                all_solutions.append(solution)
            self.update_pheromones(all_solutions, decay)

        best_solution = max(all_solutions, key=lambda x: x[1])
        return best_solution[0]

    def construct_solution(self, board, alpha, beta):
        valid_locations = self.get_valid_locations(board)
        probabilities = self.calculate_probabilities(valid_locations, alpha, beta)
        col = np.random.choice(valid_locations, p=probabilities)
        score = self.evaluate_move(board, col)
        return col, score

    def calculate_probabilities(self, valid_locations, alpha, beta):
        pheromones = np.array([self.pheromone[5][col] for col in valid_locations])
        heuristic = np.array([self.heuristic_value(col) for col in valid_locations])
        probabilities = (pheromones ** alpha) * (heuristic ** beta)
        probabilities /= probabilities.sum()
        return probabilities

    def heuristic_value(self, col):
        return 1.0  # Simple heuristic: all moves are equally likely

    def evaluate_move(self, board, col):
        temp_board = board.copy()
        row = self.get_next_open_row(temp_board, col)
        self.drop_piece(temp_board, row, col, self.player)
        return self.score_position(temp_board, self.player)

    def update_pheromones(self, all_solutions, decay):
        self.pheromone *= decay
        for col, score in all_solutions:
            self.pheromone[5][col] += score

    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(7):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def is_valid_location(self, board, col):
        return board[5][col] == 0

    def get_next_open_row(self, board, col):
        for r in range(6):
            if board[r][col] == 0:
                return r

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def score_position(self, board, piece):
        score = 0
        center_array = [int(i) for i in list(board[:, 7 // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3
        for r in range(6):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(7 - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)
        for c in range(7):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(6 - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, piece)
        for r in range(6 - 3):
            for c in range(7 - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)
        for r in range(6 - 3):
            for c in range(7 - 3):
                window = [board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)
        return score

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = 1 if piece == 2 else 2
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2
        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 4
        return score