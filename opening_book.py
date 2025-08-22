# A simple opening book as a dictionary.
# Keys are FEN strings, values are lists of possible move strings in UCI format.

OPENING_BOOK = {
    # === Starting position ===
    'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1': ['e2e4', 'd2d4', 'c2c4', 'g1f3'],

    # === King's Pawn Openings (1. e4) ===
    'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1': ['e7e5', 'c7c5', 'c7c6', 'e7e6'], # e5, Sicilian, Caro-Kann, French

    # --- After 1. e4 e5 ---
    'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2': ['g1f3', 'f1c4'], # King's Knight, Bishop's Opening
    'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2': ['b8c6', 'g8f6'], # Nc6, Petroff Defense

    # -- Ruy Lopez --
    'r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3': ['f1b5'], # 3. Bb5
    'r2qkb1r/pppp1ppp/2n2n2/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 4': ['a7a6'], # 3... a6

    # -- Italian Game --
    'r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3': ['f1c4'], # 3. Bc4
    'r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3': ['f8c5', 'g8f6'], # Giuoco Piano, Two Knights
    'r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQ1RK1 w kq - 5 5': ['c2c3'],

    # --- Sicilian Defense (1. e4 c5) ---
    'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2': ['g1f3', 'c2c3'], # Open Sicilian, Alapin
    # Open Sicilian
    'rnbqkb1r/pp1ppppp/5n2/2p1P3/8/5N2/PPPP1PPP/RNBQKB1R b KQkq - 0 3': ['d7d6', 'b8c6'],
    'rnbqkb1r/pp2pp1p/3p1np1/8/3NP3/2N5/PPP2PPP/R1BQKB1R b KQkq - 1 6': ['f8g7'], # Dragon Variation

    # --- Caro-Kann Defense (1. e4 c6) ---
    'rnbqkbnr/pp2pppp/2p5/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2': ['d2d4', 'b1c3'],
    'rnbqkbnr/pp2pppp/2p5/3p4/3PP3/8/PPP2PPP/RNBQKBNR b KQkq - 0 2': ['d7d5'],
    'rnbqkbnr/pp2pp1p/2p3p1/3p4/3PP3/2N5/PPP2PPP/R1BQKBNR w KQkq - 0 4': ['e4d5'],

    # --- French Defense (1. e4 e6) ---
    'rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2': ['d2d4'],
    'rnbqkbnr/pppp1ppp/4p3/8/3PP3/8/PPP2PPP/RNBQKBNR b KQkq - 0 2': ['d7d5'],
    'rnbqkbnr/ppp2ppp/4p3/3p4/3PP3/8/PPPN1PPP/R1BQKBNR b KQkq - 1 3': ['c7c5'], # Tarrasch Variation

    # === Queen's Pawn Openings (1. d4) ===
    'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1': ['g8f6', 'd7d5'], # Indian, QGD

    # --- After 1. d4 d5 ---
    'rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2': ['c2c4'], # Queen's Gambit
    'rnbqkbnr/ppp2ppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq - 0 2': ['e7e6', 'c7c6'], # QGD, Slav
    'rnb1kbnr/pp3ppp/2p1p3/3q4/2PP4/8/PP3PPP/RNBQKBNR w KQkq - 0 4': ['b1c3'],

    # --- Indian Defenses (1. d4 Nf6) ---
    'rnbqkb1r/pppppppp/5n2/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 1 2': ['c2c4'],
    'rnbqkb1r/pppppp1p/5np1/8/2PP4/8/PP2PPPP/RNBQKBNR b KQkq - 0 2': ['e7e6', 'g7g6'], # Nimzo/etc., King's Indian
    'rnbqk2r/ppppppbp/5np1/8/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 1 3': ['b1c3'],

    # === English Opening (1. c4) ===
    'rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1': ['e7e5', 'g8f6'],

    # === Réti Opening (1. Nf3) ===
    'rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b KQkq - 1 1': ['d7d5'],
}
