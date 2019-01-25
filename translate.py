#!/usr/bin/env python3

# Train network to play as black?

import numpy as np
import chess
import chess.pgn
import os

# Translate result to Y 
def translate_res(pgn_game):
    result = pgn_game.headers["Result"]
    y = {"0-1":-1, "1/2-1/2":0, "1-0":1}[result]
    return y


def serialize(move):
    pass

def translate_moves(game):
    pass

def parse_data(num_games = 100):

    Y = []
    X = []
    #for fname in os.listdir("data"):
    
    fname = os.listdir("data")[0]
    print("Parsing", fname, "...")
    
    n = 0
    with open(os.path.join("data", fname)) as f:
        while True:
            try:
                game = chess.pgn.read_game(f)

                result = game.headers["Result"]
                moves = game.mainline_moves()
                Y.append(translate_res(game))
                
                
                n += 1
            except:
                break
            if n > num_games:
                break
    return X, Y


if __name__ == "__main__":
    X, Y = parse_data(num_games = 10)
    print(X)
    print(Y)

