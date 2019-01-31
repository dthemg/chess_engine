#!/usr/bin/env python3

import numpy as np
from keras.models import load_model
from keras import backend as K
import os
import chess
import chess.svg
import re
import serialize
from flask import Flask, render_template, Markup, request, session

app = Flask(__name__)

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8']

def human_make_move(board):
    move_uci = input('Make move:')
    board.push_uci(move_uci)
    return board

def reverse_uci(uci_string):
    print('Incoming', uci_string)
    rev_str = []
    for ch in uci_string:
        if ch in letters:
            rev_str.append(letters[letters.index(ch)]) # < ----- Stupid line
        elif ch in numbers:
            rev_str.append(numbers[7 - numbers.index(ch)])
    print('Outgoing', ''.join(rev_str))
    return ''.join(rev_str)


def engine_make_move(board):
    
    # Load model <--- Really shouldn't be done here...
    mod = load_model(os.path.join('models', 'seq_587_3ep.h5'))

    # Black's turn?
    mirror_board = not board.turn

    # If black moves mirror board
    if mirror_board:
        board = board.mirror()    
    scores = []

    # Generate scores for all legal moves
    for lmove in board.legal_moves:
        print('Evaluating... ', lmove.uci())
        board_copy = board.copy()
        board_copy.push(lmove)
        ser_board = np.asarray(serialize.serialize_board(board_copy))
        
        scores.append({
                'move': lmove,
                'score': mod.predict(ser_board.reshape(1,-1))
                })
    best_move = sorted(scores, key = lambda ev: ev['score'], reverse=True)[0]['move']
    move_uci = best_move.uci()
    
    
    # If black moved mirror board back
    if mirror_board:
        move_uci = reverse_uci(move_uci)

    K.clear_session()
    return move_uci


@app.route('/')
def start_page():
    return render_template('index.html')

@app.route('/board')
def board_page():
    board = chess.Board()
    session['board'] = board.fen()
    
    return update_new_moves(board)

@app.route('/board', methods = ['POST', 'GET'])
def board_move():
    
    #print(session.get('board'))
    #board = chess.Board().set_fen(session.get('board'))

    if request.method == 'POST':
        user_move = request.form['user_move']
        #try:
        
        # Human makes move
        board.push_uci(user_move)

        # Computer makes move
        print(board)
        eng_move = engine_make_move(board)
        board.push_uci(eng_move)
        #except ValueError:
            #print('Not legal')
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
    app.secret_key = 'aligator3'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()

#mod = load_model(os.path.join('models', 'seq_587_3ep.h5'))
#print('Hello you')
    
    #play_human(mod)


#
