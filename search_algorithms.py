from data_loader import load_pgn_database
import re
import time


# first search algorithm, rabin karp search
def rabin_karp_search(pattern, text, base=256, mod=101):
    n, m = len(text), len(pattern)
    if m > n:
        return False

    p_hash = t_hash = 0
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


#second search algorithm, KMP search, since James didn't do it we were intrustced to use a search from a library that already exists
def kmp_search(pattern: str, text: str) -> bool:
    #Perform substring search using Python's regex engine which is equivalent to a KMP-style linear search.
    return re.search(re.escape(pattern), text) is not None


def compare_moves(input_game: str, database_game: str, method="rabin-karp") -> int:
    input_moves = input_game.split()
    score = 0

    for move in input_moves:
        if method == "kmp":
            found = kmp_search(move, database_game)
        else:
            found = rabin_karp_search(move, database_game)

        if found:
            score += 1
    return score


def longest_sequence(input_game: str, database_game: str) -> int:
    input_moves = input_game.split()
    db_moves = database_game.split()
    longest = 0

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


def compare_games(input_game: str, database_game: str, mode="moves", method="rabin-karp") -> int:
    if mode == "moves":
        return compare_moves(input_game, database_game, method)
    elif mode == "sequence":
        return longest_sequence(input_game, database_game)
    else:
        raise ValueError("Mode must be 'moves' or 'sequence'")


def find_most_similar_game(input_game: str, database_games, mode="moves", method="rabin-karp"):
    start = time.perf_counter()
    
    best_score = -1
    best_game = None

    for idx, game in enumerate(database_games):
        score = compare_games(input_game, game, mode, method)
        if score > best_score:
            best_score = score
            best_game = game

    elapsed = time.perf_counter() - start  
    print(f"{method.upper()} search completed in {elapsed:.2f} seconds")

    return best_game, best_score