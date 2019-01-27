#!/usr/bin/env python3

import numpy as np
import chess
import chess.pgn
import os
import re
import h5py

# fen representaiton
fen_chs = ['r', 'R', 'n', 'N', 'b', 'B', 'q', 'Q', 'k', 'K', 'p', 'P']

fen_ch2lay = {'r':0, 'n':1, 'b':2, 'q':3, 'k':4, 'p':5,
              'R':6, 'N':7, 'B':8, 'Q':9, 'K':10, 'P':11}


def serialize(board):
    fen_rep = board.board_fen().strip("/")
    fen_rep = re.sub('/', '', fen_rep)
    ser = np.zeros((64, 12), dtype='bool')

    ind = 0
    for char in fen_rep:
        if char in fen_chs:
            ser[ind, fen_ch2lay[char]] = 1
            ind += 1
        else:
            ind += int(char)
    # TODO: Castling rights, en passant? 
    return ser.flatten()     

def serialize_game(game):
    serialized_moves = []
    serialized_results = []
    board = chess.Board()
    moves = game.mainline_moves()
    
    res = game.headers["Result"]
    y_rep = {"0-1":-1, "1/2-1/2":0, "1-0":1}[res]

    for move in moves:
        serialized_moves.append(serialize(board))
        serialized_results.append(y_rep)
        board.push(move)
    return serialized_moves, serialized_results
        
def parse_data(num_games = 100):

    Y = []
    X = []
    
    fnames = os.listdir("data")
    
    n = 0
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
    return np.asarray(X), np.asarray(Y)


if __name__ == "__main__":
    X, Y = parse_data(num_games = 100)
    h5f = h5py.File(os.path.join('serialized_data', 'serialized_100.h5'), 'w')
    h5f.create_dataset('X', data=X)
    h5f.create_dataset('Y', data=Y)
    h5f.close()
        
