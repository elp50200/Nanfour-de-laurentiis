import numpy as np


class Player:
    def __init__(self, playerOne):
        self.simState = None
        if playerOne:
            self.player = 1
            self.oppo = 2
        else:
            self.player = 2
            self.oppo = 1
        self.transposition_table = {}

    def makeMove(self, gameState) -> int:
        board = np.array(gameState)
        winning_move = self.get_winning_move(board, self.player)

        if winning_move is not None:
            return winning_move

        if self.player == 1:
            col, score = self.negamax(board, 6, -np.inf, np.inf, 1)
        else:
            col, minimax_score = self.minimax(board, 5, -np.inf, np.inf, True)

        self.simMove(gameState, col)
        losing_move = self.get_winning_move(np.array(self.simState), self.oppo)
        if losing_move is None:
            return col

        new_col = self.get_valid_locations(board)
        return len(new_col) - 1


    def get_winning_move(self, board, piece):
        for col in self.get_valid_locations(board):
            row = self.get_next_open_row(board, col)
            temp_board = board.copy()
            self.drop_piece(temp_board, row, col, piece)
            if self.detect_win(temp_board, piece):
                return col
        return None

    def is_terminal_node(self, board):
        return self.detect_win(board, self.player) or self.detect_win(board, self.oppo) or len(self.get_valid_locations(board)) == 0

    def negamax(self, board, depth, alpha, beta, color):
        board_tuple = tuple(map(tuple, board))
        if board_tuple in self.transposition_table:
            return self.transposition_table[board_tuple]

        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.detect_win(board, self.player):
                    return (None, color * 100000000000000)
                elif self.detect_win(board, self.oppo):
                    return (None, color * -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, color * self.score_position(board, self.player))

        # Move ordering: prioritize center column
        center = 3
        valid_locations.sort(key=lambda x: abs(center - x))

        best_value = -np.inf
        best_column = valid_locations[0]
        for col in valid_locations:
            row = self.get_next_open_row(board, col)
            b_copy = board.copy()
            self.drop_piece(b_copy, row, col, self.player if color == 1 else self.oppo)
            _, value = self.negamax(b_copy, depth - 1, -beta, -alpha, -color)
            value = -value
            if value > best_value:
                best_value = value
                best_column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break

        self.transposition_table[board_tuple] = (best_column, best_value)
        return best_column, best_value

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.detect_win(board, self.player):
                    return (None, 100000000000000)
                elif self.detect_win(board, self.oppo):
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.score_position(board, self.player))

        # Move ordering: prioritize center column
        center = 3
        valid_locations.sort(key=lambda x: abs(center - x))

        if maximizingPlayer:
            value = -np.inf
            column = np.random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.player)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value
        else:  # Minimizing player
            value = np.inf
            column = np.random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.oppo)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

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

    def detect_win(self, board, piece):
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

    def score_position(self, board, piece):
        score = 0
        # Score center column
        center_array = [int(i) for i in list(board[:, 7 // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3
        # Score Horizontal
        for r in range(6):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(7 - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)
        # Score Vertical
        for c in range(7):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(6 - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, piece)
        # Score positive sloped diagonal
        for r in range(6 - 3):
            for c in range(7 - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)
        # Score negative sloped diagonal
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

    def simMove(self, gameState, col):
        if col < 0 or col > 6:
            return False
        for row in range(6):
            if gameState[row][col] == 0:
                self.simState = gameState
                self.simState[row][col] = self.player
                return True
        return False