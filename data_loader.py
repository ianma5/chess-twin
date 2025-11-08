import os
import io
import json
import chess.pgn
import zstandard as zstd

CACHE_FILE = "chess_cache.json"

def load_pgn_database(file_path, max_games=1000):
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    moves_list = []

    with open(file_path, 'rb') as compressed_file:
        dctx = zstd.ZstdDecompressor()
        with dctx.stream_reader(compressed_file) as reader:
            text_stream = io.TextIOWrapper(reader, encoding='utf-8', errors='ignore')

            game_count = 0
            while game_count < max_games:
                game = chess.pgn.read_game(text_stream)
                if game is None:
                    continue  

                board = game.board()
                moves = []
                try:
                    for move in game.mainline_moves():
                        san = board.san(move)
                        moves.append(san)
                        board.push(move)
                    moves_list.append(" ".join(moves))
                except Exception as e:
                    continue

                game_count += 1


    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(moves_list, f)

    return moves_list