#!/usr/bin/env python3

import h5py
import os
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras import optimizers

def load_dataset(name):
    h5f = h5py.File(os.path.join("serialized_data", name), 'r')
    X = h5f['X'][:]
    Y = h5f['Y'][:]
    h5f.close()
    return X, Y

def create_model():
    model = Sequential()
    model.add(Dense(2048, activation='relu', input_shape=(768,)))
    model.add(Dense(2048, activation='relu')
    model.add(Dense(2048, activation='relu')
    model.add(Dense(1))

def compile_model(model):
    model.compile(loss='mean_squared_error')
    

if __name__ == "__main__":
    X, Y = load_dataset("serialized_100.h5")
    print(X.shape)
    print(Y.shape)
