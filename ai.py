import chess
import time

class TimeUpError(Exception):
    pass

class ChessAI:
    def __init__(self, game):
        self.game = game
        self.opening_book = {
            'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1': 'e2e4',
            'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1': 'c7c5', # Sicilian Defense
            'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2': 'g1f3',
            'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1': 'd2d4',
            'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1': 'g8f6', # Indian Defense
        }
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }

    def evaluate_board(self, board):
        # A simple evaluation function based on material count.
        # Possible improvements:
        # 1. Piece-Square Tables (PSTs): Add a value to each piece based on its position.
        #    For example, a knight in the center is more valuable than a knight on the rim.
        # 2. Tapered evaluation: Use different PSTs for opening, middlegame, and endgame.
        # 3. Consider other factors like king safety, pawn structure, etc.
        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = self.piece_values[piece.piece_type]
                if piece.color == chess.WHITE:
                    score += value
                else:
                    score -= value
        return score

    def find_best_move(self, board, time_limit):
        fen = board.fen()
        if fen in self.opening_book:
            move_uci = self.opening_book[fen]
            return 0, chess.Move.from_uci(move_uci)

        start_time = time.time()

        # Fallback to a random move if time is very short
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return 0, None
        best_move = legal_moves[0]

        try:
            for depth in range(1, 10): # Max depth of 10
                _, move = self.alphabeta(board, depth, -float('inf'), float('inf'), board.turn, start_time, time_limit)
                if move:
                    best_move = move
        except TimeUpError:
            pass # Time is up, return the best move found so far

        return 0, best_move

    def alphabeta(self, board, depth, alpha, beta, maximizing_player, start_time, time_limit):
        if time.time() - start_time > time_limit:
            raise TimeUpError()
        # Possible improvements:
        # 1. Quiescence Search: To mitigate the horizon effect, extend the search for tactical moves
        #    (captures, checks) beyond the nominal search depth. This makes the AI less likely to
        #    fall for simple traps.
        # 2. Move Ordering: Improve the efficiency of alpha-beta pruning by searching the best moves
        #    first. A simple heuristic is to check captures and checks before quiet moves.
        if depth == 0 or board.is_game_over() or self.game.stop_ai.is_set():
            return self.evaluate_board(board), None

        best_move = None
        if maximizing_player:
            max_eval = -float('inf')
            for move in board.legal_moves:
                board.push(move)
                evaluation, _ = self.alphabeta(board, depth - 1, alpha, beta, False, start_time, time_limit)
                board.pop()
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                evaluation, _ = self.alphabeta(board, depth - 1, alpha, beta, True, start_time, time_limit)
                board.pop()
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval, best_move
