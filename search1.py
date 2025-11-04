from data_loader import load_pgn_database
games = load_pgn_database("lichess_db_standard_rated_2013-01.pgn.zst", max_games=1000)
print("Example:", games[0][:100])

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
        if p_hash == t_hash and text[i:i + m] == pattern:
            return True

        if i < n - m:
            t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % mod
            t_hash = (t_hash + mod) % mod 

    return False


def compare_games(input, data):
    moves = input.split()
    score = 0

    for move in moves:
        if rabin_karp_search(move, data) == True:
            score += 1

    return score


def find_most_similar_game(input_game, database_games):
    scores = []
    for game in database_games:
        score = compare_games(input_game, game)
        scores.append(score)

    best_index = scores.index(max(scores))
    return database_games[best_index], max(scores)

# def main():
#     games = [
#         "e4 e5 Nf3 Nc6 a6 Ba4",
#         "d4 d5 c4 Nf6 Nc3 Be7",
#         "e4 c5 Nf3 d6 d4 cxd4 Nxd4 Nf6",
#         "Bb5 e4 e5 Nf3 Nc6 Bc4 Nf6"
#     ]

#     input_game = "e4 e5 Nf3 Nc6 Bb5"
#     best_game, score = find_most_similar_game(input_game, games)

#     print("\nInput Game:")
#     print(input_game)
#     print("\nMost Similar Game:")
#     print(best_game)
#     print(f"\nShared Moves: {score} out of {len(input_game.split())}")

# if __name__ == "__main__":
#     main()