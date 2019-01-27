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
                        print(k)

                    if n > num_games:
                        break
                else:
                    break


    ''' 
    for fname in fnames:
        if n < num_games:
            print("Parsing %s..." % fname)
        else:
            break
        
        with open(os.path.join("data", fname)) as f:
            while True:
            #try:
                game = chess.pgn.read_game(f)
            
                X_game, Y_game = serialize_game(game)
                Y.extend(Y_game)
                X.extend(X_game)
                n += 1
                
                if n % 1000 == 0:
                    print("\t%i..." % n)
                if n >= num_games:
                    break
             #   except:
             #       print("Opsie")
             #       break


    print("Successfully parsed %i games" % n)
    '''
    return 1, 2
    

if __name__ == "__main__":
    make_low_rated_file(num_games = 10000)
        
