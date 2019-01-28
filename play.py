#!/usr/bin/env python3

import numpy as np
from keras.models import load_model
import os
import chess
import re

import serialize


# Fix Black illegal moves
def engine_play(mod, board):

    # If black moves mirror board
    if board.turn == 0:
        board = board.mirror()
    
    
    scores = []

    # Generate scores for all legal moves
    for lmove in board.legal_moves:
        board_copy = board.copy()
        board_copy.push(lmove)
        ser_board = np.asarray(serialize.serialize_board(board_copy))
        scores.append({
                'move': lmove,
                'score': mod.predict(ser_board.reshape(1,-1))
                })
    sorted_moves = sorted(scores, key = lambda ev: ev['score'], reverse=True)
    print(sorted_moves) 
    best_move = sorted_moves[0]['move']
    return best_move

def play_human(mod):
    board = chess.Board()
    while True:
        if not board.is_game_over():
            move = engine_play(mod, board)
            print('Computer moves')
            board.push(move)
            print(board)
        if not board.is_game_over():
            move = input('Make move:')
            board.push_san(move)
            print(board)
        
        


if __name__ == '__main__':
    mod = load_model(os.path.join('models', 'seq_587_3ep.h5'))
    play_human(mod)


