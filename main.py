import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import os
from datetime import timedelta

try:
    import chess
except ImportError:
    chess = None

from board_ui import ChessBoard, ChessPieces
from game_ui import GameUI
from ai import ChessAI, TimeUpError

class ChessGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Chess Game")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.board = chess.Board()
        self.selected_square = None
        self.dragged_piece = None
        self.dragged_piece_item = None
        self.player_color = chess.WHITE
        self.ai_move_queue = queue.Queue()
        self.ai_thread = None
        self.stop_ai = threading.Event()

        self.white_time = None
        self.black_time = None
        self.timer_running = False
        self.timer_id = None

        self.white_captured = []
        self.black_captured = []

        # Create main frame
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create UI components
        self.create_widgets()
        self.chess_ai = ChessAI(self)
        self.new_game()

    def create_widgets(self):
        self.board_canvas = ChessBoard(self.main_frame)
        self.board_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.board_canvas.bind("<Button-1>", self.on_mouse_down)
        self.board_canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.board_canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        self.game_ui = GameUI(self.main_frame, self)
        self.game_ui.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

    def update_board(self):
        self.board_canvas.draw_pieces(self.board)
        self.update_status()
        self.master.update_idletasks()

    def on_mouse_down(self, event):
        self.board_canvas.clear_highlights()
        if self.board.turn != self.player_color:
            return

        col = event.x // self.board_canvas.square_size
        row = 7 - (event.y // self.board_canvas.square_size)
        self.selected_square = chess.square(col, row)

        piece = self.board.piece_at(self.selected_square)
        if piece and piece.color == self.board.turn:
            self.dragged_piece = piece
            self.dragged_piece_item = self.board_canvas.create_text(
                event.x, event.y, text=ChessPieces.get_symbol(piece),
                font=("TkDefaultFont", 48), fill=self.board_canvas.get_piece_color(piece)
            )
            self.board_canvas.hide_piece(self.selected_square)


    def on_mouse_drag(self, event):
        if self.dragged_piece_item:
            self.board_canvas.coords(self.dragged_piece_item, event.x, event.y)

    def on_mouse_up(self, event):
        if self.dragged_piece_item:
            self.board_canvas.delete(self.dragged_piece_item)
            self.dragged_piece_item = None

            col = event.x // self.board_canvas.square_size
            row = 7 - (event.y // self.board_canvas.square_size)
            to_square = chess.square(col, row)

            move = chess.Move(self.selected_square, to_square)
            if self.board.piece_at(self.selected_square).piece_type == chess.PAWN and \
               chess.square_rank(to_square) in [0, 7]:
                move.promotion = self.ask_promotion_piece()

            if move in self.board.legal_moves:
                self.handle_capture(move)
                san_move = self.board.san(move)
                self.board.push(move)
                self.append_san_to_notation(san_move)
                self.trigger_ai_move()

            self.update_board() # Redraw board to show the piece in its final position
            self.dragged_piece = None
            self.selected_square = None

    def trigger_ai_move(self):
        if not self.board.is_game_over() and self.board.turn != self.player_color:
            self.game_ui.ai_status_label.config(text="AI is thinking...")
            selected_level = self.game_ui.ai_difficulty_var.get()
            level_index = self.game_ui.ai_levels.index(selected_level)
            time_limits = [0.5, 1, 2, 5, 10]
            time_limit = time_limits[level_index]

            self.ai_thread = threading.Thread(target=self.run_ai_move, args=(time_limit,))
            self.ai_thread.start()
            self.master.after(100, self.check_ai_move)

    def run_ai_move(self, time_limit):
        _, move = self.chess_ai.find_best_move(self.board.copy(), time_limit)
        self.ai_move_queue.put(move)

    def check_ai_move(self):
        try:
            move = self.ai_move_queue.get_nowait()
            if move:
                self.handle_capture(move)
                san_move = self.board.san(move)
                self.board.push(move)
                self.update_board()
                self.append_san_to_notation(san_move)
                self.game_ui.ai_status_label.config(text="")
            else:
                # If move is None, it might be a bug or game over. Stop polling.
                self.game_ui.ai_status_label.config(text="AI move is None.")
        except queue.Empty:
            self.master.after(100, self.check_ai_move)

    def handle_capture(self, move):
        captured_piece = None
        if self.board.is_en_passant(move):
            captured_piece = chess.Piece(chess.PAWN, not self.board.turn)
        elif self.board.is_capture(move):
            captured_piece = self.board.piece_at(move.to_square)

        if captured_piece:
            symbol = ChessPieces.get_symbol(captured_piece)
            if captured_piece.color == chess.WHITE:
                self.black_captured.append(symbol)
            else:
                self.white_captured.append(symbol)
            self.update_captured_pieces_display()

    def update_captured_pieces_display(self):
        white_text = "White: " + "".join(sorted(self.white_captured))
        black_text = "Black: " + "".join(sorted(self.black_captured))
        self.game_ui.white_captured_label.config(text=white_text)
        self.game_ui.black_captured_label.config(text=black_text)

    def ask_promotion_piece(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Pawn Promotion")

        piece_frame = tk.Frame(dialog)
        piece_frame.pack(padx=10, pady=10)

        result = tk.IntVar()
        result.set(chess.QUEEN)

        ttk.Radiobutton(piece_frame, text="Queen", value=chess.QUEEN, variable=result).pack(anchor=tk.W)
        ttk.Radiobutton(piece_frame, text="Rook", value=chess.ROOK, variable=result).pack(anchor=tk.W)
        ttk.Radiobutton(piece_frame, text="Bishop", value=chess.BISHOP, variable=result).pack(anchor=tk.W)
        ttk.Radiobutton(piece_frame, text="Knight", value=chess.KNIGHT, variable=result).pack(anchor=tk.W)

        ok_button = ttk.Button(dialog, text="OK", command=dialog.destroy)
        ok_button.pack(pady=5)

        dialog.transient(self.master)
        dialog.grab_set()
        self.master.wait_window(dialog)

        return result.get()

    def new_game(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
        self.clear_notation_history()
        self.white_captured.clear()
        self.black_captured.clear()
        self.update_captured_pieces_display()
        self.board.reset()
        self.board_canvas.clear_highlights()
        time_str = self.game_ui.time_var.get().split()[0]
        time_minutes = int(time_str)
        self.white_time = timedelta(minutes=time_minutes)
        self.black_time = timedelta(minutes=time_minutes)
        self.timer_running = True
        self.update_timers()
        self.update_board()
        if self.board.turn != self.player_color:
            self.trigger_ai_move()

    def switch_sides(self):
        self.player_color = not self.player_color
        self.new_game()

    def update_timers(self):
        if not self.timer_running or self.board.is_game_over():
            return

        if self.board.turn == chess.WHITE:
            self.white_time -= timedelta(seconds=1)
            if self.white_time.total_seconds() <= 0:
                self.end_game("Black wins on time")
                return
        else:
            self.black_time -= timedelta(seconds=1)
            if self.black_time.total_seconds() <= 0:
                self.end_game("White wins on time")
                return

        self.game_ui.white_time_label.config(text=f"White: {str(self.white_time).split('.')[0]}")
        self.game_ui.black_time_label.config(text=f"Black: {str(self.black_time).split('.')[0]}")

        self.timer_id = self.master.after(1000, self.update_timers)

    def end_game(self, message):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_running = False
        messagebox.showinfo("Game Over", message)

    def resign_game(self):
        messagebox.showinfo("Game Over", "You resigned. Game over.")
        self.new_game()

    def show_legal_moves(self):
        if self.selected_square is not None:
            legal_moves = [move for move in self.board.legal_moves if move.from_square == self.selected_square]
            self.board_canvas.highlight_legal_moves(legal_moves)

    def copy_notation_to_clipboard(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.game_ui.notation_text.get(1.0, tk.END))
        messagebox.showinfo("Copied", "Move notation copied to clipboard.")

    def clear_notation_history(self):
        self.game_ui.notation_text.config(state='normal')
        self.game_ui.notation_text.delete(1.0, tk.END)
        self.game_ui.notation_text.config(state='disabled')

    def update_status(self):
        if self.board.is_checkmate():
            status = f"Checkmate! {'Black' if self.board.turn == chess.WHITE else 'White'} wins."
        elif self.board.is_stalemate():
            status = "Stalemate! Draw."
        elif self.board.is_insufficient_material():
            status = "Insufficient material. Draw."
        elif self.board.is_seventyfive_moves():
            status = "75-move rule. Draw."
        elif self.board.is_fivefold_repetition():
            status = "Fivefold repetition. Draw."
        elif self.board.is_check():
            status = f"{'White' if self.board.turn == chess.WHITE else 'Black'}'s turn (in check)"
        else:
            status = f"{'White' if self.board.turn == chess.WHITE else 'Black'}'s turn"
        self.game_ui.status_label.config(text=status)

    def append_san_to_notation(self, san_move):
        self.game_ui.notation_text.config(state='normal')
        move_num = (len(self.board.move_stack) + 1) // 2
        if self.board.turn == chess.BLACK: # White's move was just made
            self.game_ui.notation_text.insert(tk.END, f"{move_num}. {san_move} ")
        else: # Black's move was just made
            self.game_ui.notation_text.insert(tk.END, f"{san_move}\n")
        self.game_ui.notation_text.config(state='disabled')
        self.game_ui.notation_text.see(tk.END)


    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.stop_ai.set()
            if self.ai_thread and self.ai_thread.is_alive():
                self.ai_thread.join()
            self.master.destroy()
            os._exit(0)

if __name__ == "__main__":
    if chess is None:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", "python-chess library not found. Please install it to play.")
    else:
        root = tk.Tk()
        game = ChessGame(root)
        root.mainloop()
