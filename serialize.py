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


def serialize_board(board):
    fen_rep = board.board_fen().strip("/")
    fen_rep = re.sub('/', '', fen_rep)
    ser = np.zeros((64, 12), dtype='bool')

    # Board positions
    ind = 0
    for char in fen_rep:
        if char in fen_chs:
            ser[ind, fen_ch2lay[char]] = 1
            ind += 1
        else:
            ind += int(char) 
    ser = ser.flatten()
   
   # Castling rights
    cast = np.array([
                board.has_kingside_castling_rights(0),
                board.has_queenside_castling_rights(0),
                board.has_kingside_castling_rights(1),
                board.has_queenside_castling_rights(1)],
                dtype='bool')
    
    ser = np.concatenate([ser, cast], axis=0)
    return ser

def serialize_game(game):
    serialized_moves = []
    serialized_results = []
    board = chess.Board()
    moves = game.mainline_moves()
    
    res = game.headers["Result"]
    y_rep = {"0-1":-1, "1/2-1/2":0, "1-0":1}[res]

    for move in moves:
    
        if board.turn == 0:
            # Black moves
            board_mir = board.mirror()
            serialized_moves.append(serialize_board(board_mir))
            serialized_results.append(y_rep*-1)
        else:
            # White moves
            serialized_moves.append(serialize_board(board))
            serialized_results.append(y_rep)
        board.push(move)
    return serialized_moves, serialized_results

def serialize_pgn_file():
    n_ser = 0
    X_ser = []
    Y_ser = []
    with open(os.path.join('data', 'lichess_db_sub1200.pgn')) as pgn_file:
        while True:

            game = chess.pgn.read_game(pgn_file)
            if game is not None:
                n_ser += 1
                ser_moves, ser_results = serialize_game(game)
                X_ser.extend(ser_moves)
                Y_ser.extend(ser_results)
                
            else:
                break
    print('Successfully parsed %i games' % n_ser)
    return np.asarray(X_ser), np.asarray(Y_ser)
        
    
if __name__ == '__main__':
    X, Y = serialize_pgn_file() 
    
    fp = os.path.join('serialized_data', 'serialized_587.h5')
    h5f = h5py.File(fp, 'w')
    h5f.create_dataset('X', data=X)
    h5f.create_dataset('Y', data=Y)
    h5f.close()
    print('Successfully wrote to file:', fp)


