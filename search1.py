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