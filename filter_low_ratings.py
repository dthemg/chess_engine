#!/usr/bin/env python3

import numpy as np
import chess
import chess.pgn
import os
import re

def make_low_rated_file(num_games = 100):

    all_ratings = os.path.join('data', 'lichess_db.pgn')

    with open(os.path.join('data', 'lichess_db_sub1200.pgn'), 'a', encoding='utf-8') as lrf:
        exporter = chess.pgn.FileExporter(lrf)
        n = 0
        k = 0
        with open(all_ratings) as f:
            while True:
                game = chess.pgn.read_game(f)
                
                if game is not None:
                    n += 1
                   
                    # Check that at least one player has ELO < 1400
                    if int(game.headers['WhiteElo']) < 1200 or int(game.headers['BlackElo']) < 1200:
                        k += 1
                        game.accept(exporter)
                        if k % 100 == 0:
                            print(k)

                    if n > num_games:
                        break
                else:
                    break


if __name__ == "__main__":
    make_low_rated_file(num_games = 100000)
        
