#!/usr/bin/env python3

import numpy as np
import chess
import chess.pgn
import os
import re


# fen representaiton
fen_chs = ['r', 'R', 'n', 'N', 'b', 'B', 'q', 'Q', 'k', 'K', 'p', 'P']
fen_ch2lay = {'r': 0, 'R': 0, 'n': 1, 'N': 1, 'b': 2, 'B': 2,
                'q': 3, 'Q': 3, 'k':4, 'K': 4, 'p': 5, 'P': 5}
fen_ch2val = {'r': -1, 'R': 1, 'n': -1, 'N': 1, 'b': -1, 'B': 1,
                'q': -1, 'Q': 1, 'k': -1, 'K': 1, 'p': -1, 'P': 1}

# Translate result to Y 
def translate_res(pgn_game):
    result = pgn_game.headers["Result"]
    y = {"0-1":-1, "1/2-1/2":0, "1-0":1}[result]
    return y

def serialize(board):
    fen_rep = board.board_fen().strip("/")
    fen_rep = re.sub('/', '', fen_rep)
    ser = np.zeros((64,6))
    ind = 0
    for char in fen_rep:
        if char in fen_chs:
            ser[ind, fen_ch2lay[char]] = fen_ch2val[char]
            ind += 1
        else:
            ind += int(char)
    return ser.reshape(8,8,6) 
    

def translate_moves(game):
    board = chess.Board()
    moves = game.mainline_moves()
    for move in moves:
        #print(board.board_fen())    
        #print(board)
        print(serialize(board)[:,:,-1])
        board.push(move)
        print("###")

def parse_data(num_games = 100):

    Y = []
    X = []

    #for fname in os.listdir("data"): 
    fname = os.listdir("data")[0]
    print("Parsing", fname, "...")
    
    n = 0
    with open(os.path.join("data", fname)) as f:
        while True:
            #try:
            game = chess.pgn.read_game(f)

            result = game.headers["Result"]
            moves = game.mainline_moves()
            Y.append(translate_res(game))
            translate_moves(game)
            n += 1
            #except Exception:
            #    break
            if n >= num_games:
                break
    return np.asarray(X), np.asarray(Y)


if __name__ == "__main__":
    X, Y = parse_data(num_games = 1)
    print(X)
    print(Y)

