def rabin_karp_search(pattern, text, base=256, mod=101):
    """
    Returns True if 'pattern' is found anywhere in 'text' using rolling hash.
    """
    n = len(text)
    m = len(pattern)
    if m > n:
        return False

    p_hash = 0  # pattern hash
    t_hash = 0  # text window hash
    h = pow(base, m - 1, mod)

    # Calculate initial hash for pattern and first window of text
    for i in range(m):
        p_hash = (base * p_hash + ord(pattern[i])) % mod
        t_hash = (base * t_hash + ord(text[i])) % mod

    # Slide the pattern over the text
    for i in range(n - m + 1):
        # If hashes match, verify substring directly
        if p_hash == t_hash and text[i:i + m] == pattern:
            return True

        # Roll the hash forward (remove one char, add next)
        if i < n - m:
            t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % mod
            t_hash = (t_hash + mod) % mod  # ensure positive hash

    return False


# --------------------------------------------------------
# Compare two games: one move at a time (partial matching)
# --------------------------------------------------------
def compare_games(input_game, database_game):
    """
    Compares two chess games by checking if each move in the input_game
    appears anywhere in the database_game.
    Returns a score equal to the number of moves that match.
    """
    input_moves = input_game.split()
    db_game = database_game
    score = 0

    for move in input_moves:
        if rabin_karp_search(move, db_game):
            score += 1

    return score


# --------------------------------------------------------
# Find the most similar game in a database
# --------------------------------------------------------
def find_most_similar_game(input_game, database_games):
    scores = []
    for game in database_games:
        score = compare_games(input_game, game)
        scores.append(score)

    best_index = scores.index(max(scores))
    return database_games[best_index], max(scores)


# --------------------------------------------------------
# Example usage
# --------------------------------------------------------
def main():
    # Example dataset (you can replace this with your real chess games)
    games = [
        "e4 e5 Nf3 Nc6 a6 Ba4",
        "d4 d5 c4 Nf6 Nc3 Be7",
        "e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6",
        "Bb5 e4 e5 Nf3 Nc6 Bc4 Nf6"
    ]

    input_game = "e4 e5 Nf3 Nc6 Bb5"
    best_game, score = find_most_similar_game(input_game, games)

    print("\nInput Game:")
    print(input_game)
    print("\nMost Similar Game:")
    print(best_game)
    print(f"\nShared Moves: {score} out of {len(input_game.split())}")

if __name__ == "__main__":
    main()