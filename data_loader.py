import os
import io
import json
import chess.pgn
import zstandard as zstd

CACHE_FILE = "chess_cache.json"

def load_pgn_database(file_path, max_games=1000):
    if os.path.exists(CACHE_FILE):
        #print(" Loading cached PGN data...")
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        #print(f" Loaded {len(data)} games from cache.")
        return data

    #print(" Parsing PGN database, this may take several minutes...")
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
                    #print(f"Skipping invalid game #{game_count + 1}: {e}")
                    continue

                game_count += 1

                #if game_count % 1000 == 0:
                    #print(f"Loaded {game_count} games...")

    #print(f"Finished parsing {len(moves_list)} games.")

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(moves_list, f)

    #print(f" Saved cache to {CACHE_FILE}.")
    return moves_list