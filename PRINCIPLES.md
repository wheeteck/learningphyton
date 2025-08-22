# Design for a Principles-Based Chess AI

This document outlines the design for an AI engine that makes moves based on fundamental chess principles rather than a deep, brute-force search. This engine is intended for the opening phase of the game and aims to play in a "human-like", logical manner.

The core idea is to score each legal move based on a set of heuristics derived from these principles. The AI will then choose the move with the highest score.

---

### **Top 20 Opening Principles & Implementation Strategy**

Here is a list of common opening principles and a suggested strategy for how to codify them. Each principle can be a function that returns a score (positive for good, negative for bad) for a given move.

**A. Center Control**
1.  **Occupy the Center with a Pawn:**
    *   **Principle:** Control the center squares (d4, e4, d5, e5).
    *   **Implementation:** Give a high score to moves that place a pawn on one of these squares (e.g., `e2e4`, `d7d5`).
2.  **Control the Center with Pieces:**
    *   **Principle:** If you can't occupy the center, control it with your pieces.
    *   **Implementation:** Score moves based on the number of center squares they attack. A knight move to `f3` attacks `d4` and `e5`.
3.  **Challenge Opponent's Center:**
    *   **Principle:** Don't let your opponent have uncontested control of the center.
    *   **Implementation:** Give a bonus to moves that attack the opponent's central pawns.

**B. Piece Development**
4.  **Develop Knights Before Bishops:**
    *   **Principle:** Knights are less flexible than bishops, so it's often clear where they should go early on.
    *   **Implementation:** Give a higher score to knight development moves than bishop development moves in the first few turns.
5.  **Develop Towards the Center:**
    *   **Principle:** Pieces are more powerful when they are closer to the center.
    *   **Implementation:** Score development moves higher if their destination square is closer to the center.
6.  **Don't Move the Same Piece Twice:**
    *   **Principle:** Wasting time (tempo) in the opening is bad. Develop a new piece instead.
    *   **Implementation:** Give a significant penalty to any move of a piece that has already moved (unless it's the king for castling).
7.  **Develop with a Threat:**
    *   **Principle:** Combine development with an attack to put pressure on the opponent.
    *   **Implementation:** Give a bonus to development moves that also create a direct attack on an opponent's piece.
8.  **Don't Bring the Queen Out Too Early:**
    *   **Principle:** The queen is a valuable piece and can become a target for the opponent's developing pieces.
    *   **Implementation:** Give a large penalty to queen moves in the first ~8-10 moves, unless the move is forced or gives a significant advantage (like a check).
9.  **Connect the Rooks:**
    *   **Principle:** A key goal of the opening is to get your rooks to see each other, which usually happens after all minor pieces are developed and you have castled.
    *   **Implementation:** Give a small bonus to the final move that "connects" the rooks (i.e., clears the back rank between them).

**C. King Safety**
10. **Castle Early:**
    *   **Principle:** Get your king to safety and bring a rook into the game.
    *   **Implementation:** Give a very high score to castling moves (`e1g1`, `e1c1`, etc.).
11. **Don't Move Pawns in Front of Your Castled King:**
    *   **Principle:** Moving the pawns that shield your king creates weaknesses.
    *   **Implementation:** Give a penalty to moves of the f, g, or h-pawns (or a, b, c-pawns for queenside castling) after the king has castled on that side.
12. **Control a Fleeing Square for the King:**
    *   **Principle:** Ensure your king has an escape route if attacked.
    *   **Implementation:** (More complex) Could be a small bonus for moves that open up a "luft" (e.g., h3 or g3).

**D. Pawn Structure**
13. **Avoid Doubled Pawns:**
    *   **Principle:** Doubled pawns (two of your pawns on the same file) are often a structural weakness.
    *   **Implementation:** Give a penalty to any capture that results in doubled pawns.
14. **Create Pawn Islands:**
    *   **Principle:** Fewer pawn islands (groups of connected pawns) is generally better.
    *   **Implementation:** (Complex) Penalize moves that break up your pawn structure.
15. **Make Favorable Trades:**
    *   **Principle:** Trade your non-central pawns for your opponent's central pawns.
    *   **Implementation:** Give a bonus for captures where a wing pawn (e.g., c-pawn) captures a center pawn (e.g., d-pawn).

**E. General Heuristics**
16. **A Knight on the Rim is Dim:**
    *   **Principle:** Knights are least effective on the edge of the board.
    *   **Implementation:** Give a penalty for moving a knight to the 'a' or 'h' files.
17. **Place Rooks on Open or Semi-Open Files:**
    *   **Principle:** Rooks are most powerful on files that are not obstructed by pawns.
    *   **Implementation:** Give a bonus to moves that place a rook on a file with no friendly pawns, and a larger bonus if there are no pawns of either color.
18. **Develop Your Least Active Pieces:**
    *   **Principle:** Improve the position of the piece that has the fewest options.
    *   **Implementation:** (Complex) Calculate the number of legal moves for each piece. Give a bonus to moves of the piece with the fewest available squares.
19. **Avoid Unnecessary Checks:**
    *   **Principle:** A check that is easily blocked or parried without the opponent making concessions often just helps them develop.
    *   **Implementation:** Score checking moves based on the quality of the opponent's likely replies. Penalize checks that can be blocked by a developing move.
20. **Maintain the Tension:**
    *   **Principle:** Don't be in a hurry to resolve a situation (like releasing a pin or making a capture) if the current state of tension benefits you.
    *   **Implementation:** (Very complex) This is difficult to codify and is likely beyond the scope of a simple principles-based engine. It would require a deeper understanding of tactical and positional nuances.
