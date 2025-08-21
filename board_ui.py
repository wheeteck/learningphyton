import tkinter as tk
import chess

class ChessBoard(tk.Canvas):
    def __init__(self, master, size=480):
        super().__init__(master, width=size, height=size)
        self.size = size
        self.square_size = size // 8
        self.light_color = "#F0D9B5"
        self.dark_color = "#B58863"
        self.draw_board()

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = self.light_color if (row + col) % 2 == 0 else self.dark_color
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def draw_pieces(self, board):
        self.delete("pieces")
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                symbol = ChessPieces.get_symbol(piece)
                row, col = 7 - (square // 8), square % 8
                x = col * self.square_size + self.square_size // 2
                y = row * self.square_size + self.square_size // 2
                self.create_text(x, y, text=symbol, font=("TkDefaultFont", 48), tags=("pieces", f"piece_{square}"), fill=self.get_piece_color(piece))

    def hide_piece(self, square):
        self.itemconfig(f"piece_{square}", state='hidden')

    def highlight_legal_moves(self, moves):
        self.delete("highlight")
        for move in moves:
            row, col = 7 - (move.to_square // 8), move.to_square % 8
            x = col * self.square_size + self.square_size // 2
            y = row * self.square_size + self.square_size // 2
            self.create_oval(x - 10, y - 10, x + 10, y + 10, fill="green", tags="highlight", outline="", width=0)

    def clear_highlights(self):
        self.delete("highlight")

    def get_piece_color(self, piece):
        if piece.color == chess.WHITE:
            return "white"
        else:
            return "black"


class ChessPieces:
    PIECE_SYMBOLS = {
        'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
        'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
    }

    @staticmethod
    def get_symbol(piece):
        return ChessPieces.PIECE_SYMBOLS[piece.symbol()]
