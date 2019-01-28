#!/usr/bin/env python3

import numpy as np
from keras.models import load_model
import os
import chess
import re

import serialize




def human_make_move(board):
    move_san = input('Make move:')
    board.push_san(move_san)
    return board

def engine_make_move(mod, board):
   
    #board = board.copy()

    # Black's turn?
    mirror_board = not board.turn

    # If black moves mirror board
    if mirror_board:
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
    board.push(sorted_moves[0]['move'])
    
    # If black moved mirror board back
    if mirror_board:
        board = board.mirror()

    return board

def play_self(mod):
    board = chess.Board()
    while not board.is_game_over():
        board = engine_make_move(mod, board)
        print("-"*30)
        print(board)
    print(board.result())

def play_human(mod):
    board = chess.Board()
    while True:
        if not board.is_game_over():
            board = engine_make_move(mod, board)
            print(board)
        else:
            break
        if not board.is_game_over():
            board = human_make_move(board) 
            print(board)    
        else:
            break


if __name__ == '__main__':
    mod = load_model(os.path.join('models', 'seq_587_3ep.h5'))
    play_self(mod)


