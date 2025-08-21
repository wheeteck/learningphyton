### **Consolidated Functional Requirements: Python Tkinter Chess Game**

**1. Core Gameplay & Rules**
*   A complete, playable game of chess adhering to all standard FIDE rules.
*   **Piece Movement:** All pieces (Pawn, Rook, Knight, Bishop, Queen, King) move according to their standard rules.
*   **Special Moves:**
    *   Castling (both kingside and queenside) is correctly implemented and validated.
    *   En passant captures are correctly implemented and validated.
    *   Pawn promotion occurs when a pawn reaches the final rank, with a dialog for the user to select the promotion piece (Queen, Rook, Bishop, or Knight).
*   **Game State Detection:** The game must automatically detect and announce the following states:
    *   Check
    *   Checkmate (ending the game)
    *   Stalemate (resulting in a draw)
    *   Draw by insufficient material
    *   Draw by the 75-move rule
    *   Draw by fivefold repetition
*   **Move Validation:** The system must prevent any illegal moves, including any move that would place or leave the player's own king in check.

**2. User Interface (UI)**
*   **Chessboard:**
    *   A professional-looking, canvas-based 8x8 chessboard.
    *   Light squares must use color `#F0D9B5`.
    *   Dark squares must use color `#B58863`.
*   **Chess Pieces:**
    *   Pieces are to be displayed using large, clear Unicode characters (font size 48pt).
    *   When a piece is moved, the mouse cursor should change to a representation of the piece being dragged.
*   **Game Controls:** The UI must provide buttons for the following actions:
    *   **New Game:** Starts a new game, resetting the board and timers.
    *   **Switch Sides:** Allows the player to switch between playing as White and Black.
    *   **Show Moves:** Highlights all legal moves for a selected piece.
    *   **Resign:** Allows the current player to forfeit the game.
    *   **Exit:** Closes the application gracefully.
*   **Status Indicators:**
    *   **Player Turn:** A label must clearly indicate whose turn it is to move (e.g., "White's Turn").
    *   **Game Status:** A label must display the current game state (e.g., "Check", "Checkmate").
    *   **AI Thinking Status:** A prominent, clearly visible indicator (e.g., "AI is thinking...") must be displayed while the AI is calculating its move.
*   **Move Notation Window:**
    *   A text area displays the game's move history in Standard Algebraic Notation (SAN).
    *   Moves are appended to the window as they are made.
    *   Provides a "Copy" button to copy the entire notation to the system clipboard.
    *   Provides a "Clear" button to clear the notation history.
*   **Captured Pieces Display:**
    *   A dedicated area of the UI displays the pieces captured by each player.

**3. Player vs. AI Mode**
*   **Opponent:** The primary mode of play is a human player versus an AI opponent.
*   **Color Selection:** The player can choose to play as either White or Black.
*   **AI Difficulty:**
    *   A dropdown menu allows the player to select from 5 difficulty levels.
    *   Each level should have an estimated ELO rating displayed in the dropdown (e.g., "Level 1 (ELO ~800)").
*   **AI Behavior:**
    *   The AI must operate on a per-move time control, with the time limit determined by the selected difficulty level. This ensures the AI always responds in a timely manner.
    *   The AI should have a small, built-in opening book to play common and logical opening moves.

**4. Time Controls**
*   **Player Timers:** Each player has a dedicated countdown timer.
*   **Time Settings:** A dropdown menu allows setting the initial game time for each player (options: 1, 3, 5, 10, 15, 30 minutes).
*   **Game End by Time:** The game ends if a player's timer runs out, with the opposing player declared the winner. The timer must be reliable and accurate.
