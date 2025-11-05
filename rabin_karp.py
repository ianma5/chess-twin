from data_loader import load_pgn_database
games = load_pgn_database("lichess_db_standard_rated_2013-01.pgn.zst", max_games=1000)


def rabin_karp_search(pattern, text, base=256, mod=101):
    n = len(text)
    m = len(pattern)
    if m > n:
        return False

    p_hash = 0
    t_hash = 0
    h = pow(base, m - 1, mod)

    for i in range(m):
        p_hash = (base * p_hash + ord(pattern[i])) % mod
        t_hash = (base * t_hash + ord(text[i])) % mod

    for i in range(n - m + 1):
        if p_hash == t_hash and text[i:i+m] == pattern:
            return True
        if i < n - m:
            t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i+m])) % mod
            t_hash = (t_hash + mod) % mod
    return False



def compare_moves_individual(input_game: str, database_game: str) -> int:
    input_moves = input_game.split()
    data_text = database_game
    score = 0

    for move in input_moves:
        if rabin_karp_search(move, data_text):
            score += 1
    return score



def longest_common_sequence(input_game: str, database_game: str) -> int:
    input_moves = input_game.split()
    db_moves = database_game.split()

    longest = 0
    current = 0


    for i in range(len(input_moves)):
        for j in range(len(db_moves)):
            k = 0
            while (
                i + k < len(input_moves)
                and j + k < len(db_moves)
                and input_moves[i + k] == db_moves[j + k]
            ):
                k += 1
            longest = max(longest, k)
    return longest


def compare_games(input_game: str, database_game: str, mode="moves") -> int:
    if mode == "moves":
        return compare_moves_individual(input_game, database_game)
    elif mode == "sequence":
        return longest_common_sequence(input_game, database_game)
    else:
        raise ValueError("Mode must be either 'moves' or 'sequence'")


def find_most_similar_game(input_game: str, database_games, mode="moves"):
    best_score = -1
    best_game = None

    for idx, game in enumerate(database_games):
        score = compare_games(input_game, game, mode)
        if score > best_score:
            best_score = score
            best_game = game

        if (idx + 1) % 100 == 0:
            print(f"Compared {idx+1} games...")

    print(f"✅ Best similarity score: {best_score}")
    return best_game, best_score