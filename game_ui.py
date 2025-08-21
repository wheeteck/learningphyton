import tkinter as tk
from tkinter import ttk

class GameUI(tk.Frame):
    def __init__(self, master, game_controller):
        super().__init__(master)
        self.game_controller = game_controller
        self.create_widgets()

    def create_widgets(self):
        # Control buttons
        controls_frame = ttk.LabelFrame(self, text="Controls")
        controls_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(controls_frame, text="New Game", command=self.game_controller.new_game).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(controls_frame, text="Switch Sides", command=self.game_controller.switch_sides).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(controls_frame, text="Show Moves", command=self.game_controller.show_legal_moves).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(controls_frame, text="Resign", command=self.game_controller.resign_game).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(controls_frame, text="Exit", command=self.game_controller.on_closing).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Time control
        time_frame = ttk.LabelFrame(self, text="Time Control")
        time_frame.pack(fill=tk.X, padx=5, pady=5)
        self.time_var = tk.StringVar(value="10 min")
        time_options = ["1 min", "3 min", "5 min", "10 min", "15 min", "30 min"]
        ttk.OptionMenu(time_frame, self.time_var, time_options[3], *time_options).pack(padx=5, pady=5)

        # AI difficulty
        ai_frame = ttk.LabelFrame(self, text="AI Difficulty")
        ai_frame.pack(fill=tk.X, padx=5, pady=5)
        self.ai_difficulty_var = tk.StringVar()
        self.ai_levels = [
            "Level 1 (ELO ~800)",
            "Level 2 (ELO ~1000)",
            "Level 3 (ELO ~1200)",
            "Level 4 (ELO ~1400)",
            "Level 5 (ELO ~1600)"
        ]
        self.ai_difficulty_var.set(self.ai_levels[2]) # Default to level 3
        ttk.OptionMenu(ai_frame, self.ai_difficulty_var, self.ai_levels[2], *self.ai_levels).pack(padx=5, pady=5)

        # Timer display
        timer_frame = ttk.LabelFrame(self, text="Time")
        timer_frame.pack(fill=tk.X, padx=5, pady=5)
        self.white_time_label = ttk.Label(timer_frame, text="")
        self.white_time_label.pack(padx=5, pady=5)
        self.black_time_label = ttk.Label(timer_frame, text="")
        self.black_time_label.pack(padx=5, pady=5)

        # Captured pieces display
        captured_frame = ttk.LabelFrame(self, text="Captured Pieces")
        captured_frame.pack(fill=tk.X, padx=5, pady=5)
        self.white_captured_label = ttk.Label(captured_frame, text="White: ", wraplength=150)
        self.white_captured_label.pack(anchor='w')
        self.black_captured_label = ttk.Label(captured_frame, text="Black: ", wraplength=150)
        self.black_captured_label.pack(anchor='w')

        # Status display
        status_frame = ttk.LabelFrame(self, text="Status")
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        self.status_label = ttk.Label(status_frame, text="White's turn")
        self.status_label.pack(padx=5, pady=5)
        self.ai_status_label = ttk.Label(status_frame, text="", foreground="red", font=("TkDefaultFont", 10, "bold"))
        self.ai_status_label.pack(padx=5, pady=5)

        # Move notation
        notation_frame = ttk.LabelFrame(self, text="Move Notation")
        notation_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        notation_text_frame = tk.Frame(notation_frame)
        notation_text_frame.pack(fill=tk.BOTH, expand=True)

        self.notation_text = tk.Text(notation_text_frame, height=10, width=20, state='disabled')
        self.notation_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        notation_scrollbar = ttk.Scrollbar(notation_text_frame, orient=tk.VERTICAL, command=self.notation_text.yview)
        notation_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.notation_text['yscrollcommand'] = notation_scrollbar.set

        notation_buttons_frame = tk.Frame(notation_frame)
        notation_buttons_frame.pack(fill=tk.X)
        ttk.Button(notation_buttons_frame, text="Copy", command=self.game_controller.copy_notation_to_clipboard).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(notation_buttons_frame, text="Clear", command=self.game_controller.clear_notation_history).pack(side=tk.LEFT, padx=5, pady=5)
