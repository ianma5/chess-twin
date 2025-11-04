# rabin karp search function

def rabin_karp_search(pattern, text, base=256, mod=101):
    n, m = len(text), len(pattern)
    if m > n:
        return False
    p_hash = t_hash = 0
    h = pow(base, m-1, mod)
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

def compare_games(input_game, database_game, window=4):
    input_moves = input_game.split()
    db_moves = database_game.split()
    subsequences = get_subsequences(input_moves, window)
    
    score = 0
    for seq in subsequences:
        if rabin_karp_search(seq, database_game):
            score += 1
    return score

def find_most_similar_game(input_game, database, window=4):
    scores = []
    for game in database:
        score = compare_games(input_game, game, window)
        scores.append(score)
    
    best_index = scores.index(max(scores))
    return database[best_index], max(scores)