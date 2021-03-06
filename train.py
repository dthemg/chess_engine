#!/usr/bin/env python3

import h5py
import os
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras import optimizers
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import gc
import numpy as np
import time

def load_dataset(name):
    h5f = h5py.File(os.path.join("serialized_data", name), 'r')
    X = h5f['X'][:]
    Y = h5f['Y'][:]
    h5f.close()
    return X, Y

def create_model():
    model = Sequential()
    model.add(Dense(2048, activation='relu', input_shape=(772,)))
    model.add(Dropout(0.5))
    model.add(Dense(2048, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    return model


if __name__ == "__main__":
    X, y = load_dataset("serialized_587.h5")
    # Fix y
    y = (y+1)/2

    mod = create_model()
    mod.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
    X_tr, X_ts, y_tr, y_ts = train_test_split(X, y, test_size=0.10, shuffle=False) 
    mod.fit(X_tr, y_tr, batch_size=2048, epochs=3)
    
    y_pred = mod.predict(X_ts, verbose=1)
    print("Validation MSE:", mean_squared_error(y_ts, y_pred))
    
    mod.save(os.path.join('models', 'seq_587_3ep.h5'))
    print('Model was saved')
    
