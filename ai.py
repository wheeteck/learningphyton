import chess
import time
import random
from opening_book import OPENING_BOOK

class TimeUpError(Exception):
    pass

class ChessAI:
    def __init__(self, game):
        self.game = game
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
        # Phase 1: Opening Book
        if len(board.move_stack) < 6:
            fen = board.fen()
            if fen in OPENING_BOOK:
                move_uci = random.choice(OPENING_BOOK[fen])
                return 0, chess.Move.from_uci(move_uci)

        # Phase 2: Principled Search
        if len(board.move_stack) < 20:
            return self._find_principled_search_move(board)

        # Phase 3: Pure Engine
        return self._find_best_move_ab(board, time_limit)

    def _find_principled_search_move(self, board):
        best_moves = []
        best_score = -float('inf')

        for move in board.legal_moves:
            # Get principles score for the move
            principles_score = self._score_move_by_principles(board, move)

            # Get static evaluation of the position after the move
            temp_board = board.copy()
            temp_board.push(move)
            static_eval = self.evaluate_board(temp_board)

            # The static evaluation is from White's perspective.
            # If it's Black to move, a higher score is worse for Black.
            # We want to maximize our own score.
            if board.turn == chess.BLACK:
                static_eval = -static_eval

            # Combine scores (weights may need tuning)
            combined_score = principles_score + static_eval

            if combined_score > best_score:
                best_score = combined_score
                best_moves = [move]
            elif combined_score == best_score:
                best_moves.append(move)

        # Randomly choose from the best moves
        return 0, random.choice(best_moves) if best_moves else None


    def _find_best_move_ab(self, board, time_limit):
        start_time = time.time()

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return 0, None
        best_move = legal_moves[0]

        try:
            for depth in range(1, 10):
                _, move = self.alphabeta(board, depth, -float('inf'), float('inf'), board.turn, start_time, time_limit)
                if move:
                    best_move = move
        except TimeUpError:
            pass

        return 0, best_move

    def _score_move_by_principles(self, board, move):
        score = 0
        piece = board.piece_at(move.from_square)

        # --- Tactical Awareness ---

        # 1. Captures
        if board.is_capture(move):
            captured_piece = board.piece_at(move.to_square)
            if captured_piece: # Should not be None, but good practice to check
                score += 10 * self.piece_values[captured_piece.piece_type]

        # Create a temporary board to analyze the position *after* the move
        temp_board = board.copy()
        temp_board.push(move)

        # 2. Piece Safety
        # Check if the piece we just moved is now under attack
        if temp_board.is_attacked_by(not board.turn, move.to_square):
            score -= 10 * self.piece_values[piece.piece_type]

        # 3. Creating Threats
        # Give a small bonus for each new piece we are attacking
        for sq in chess.SQUARES:
            if temp_board.is_attacked_by(board.turn, sq) and temp_board.piece_at(sq) is not None:
                score += 1


        # --- Positional Principles ---

        # Principle: Control the center
        center_squares = [chess.E4, chess.D4, chess.E5, chess.D5]
        if move.to_square in center_squares:
            if piece.piece_type == chess.PAWN:
                score += 5 # Pawn to center is good, but not worth as much as tactical considerations
            else:
                score += 2

        # Principle: Develop minor pieces
        if piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
            is_development_move = False
            if piece.color == chess.WHITE and chess.square_rank(move.from_square) in [0, 1]:
                is_development_move = True
            elif piece.color == chess.BLACK and chess.square_rank(move.from_square) in [6, 7]:
                is_development_move = True
            if is_development_move:
                score += 4

        # Principle: Castle early
        if board.is_castling(move):
            score += 10

        # Principle: Avoid moving the same piece twice
        if len(board.move_stack) < 20 and piece.piece_type != chess.PAWN:
                for m in board.move_stack:
                    if m.from_square == move.from_square:
                        score -= 3
                        break

        # Principle: Don't bring the queen out too early
        if piece.piece_type == chess.QUEEN and len(board.move_stack) < 10:
            score -= 5

        return score

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
