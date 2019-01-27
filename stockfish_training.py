#!/usr/bin/env python3

import chess
import chess.engine
import os
import numpy as np
import h5py
import chess.pgn

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

def play_self(comp_lvl=0):
    engine = chess.engine.SimpleEngine.popen_uci('engines/stockfish/src/stockfish')
    engine.configure({'Skill Level': comp_lvl})

    for i in range(100): 
        print(i)
        board = chess.Board()
        while not board.is_game_over():
            result = engine.play(board, chess.engine.Limit(time=0.0))
            board.push(result.move)
    
    # save game if checkmate
    res = board.result()
    print(res)
        
    
    

    engine.quit()

def play_x_games():
    pass


if __name__ == "__main__":
    play_self(comp_lvl=5)

