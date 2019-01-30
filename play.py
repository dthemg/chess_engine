#!/usr/bin/env python3

import numpy as np
from keras.models import load_model
import os
import chess
import chess.svg
import re
import serialize
from flask import Flask, render_template, Markup, request

app = Flask(__name__)

def human_make_move(board):
    move_uci = input('Make move:')
    board.push_uci(move_uci)
    return board

def engine_make_move(mod, board):
    
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


@app.route('/')
def start_page():
    return render_template('index.html')

@app.route('/board', methods = ['POST', 'GET'])
def board_page():
    if board is None:
        board = chess.Board()

    if request.method == 'POST':
        user_move = request.form['user_move']
        try:
            # Human makes move
            board.push_uci(user_move)
            # Computer makes move
            board = engine_make_move(mod, board)

        except ValueError:
            print('Not a legal move') 

    return update_new_moves(board)




def update_new_moves(board):    
    my_svg = chess.svg.board(board=board)
    return render_template('board.html', svg=Markup(my_svg))

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
    board = chess.Board()
    mod = load_model(os.path.join('models', 'seq_587_3ep.h5'))
    app.run()

#mod = load_model(os.path.join('models', 'seq_587_3ep.h5'))
#print('Hello you')
    
    #play_human(mod)


#
