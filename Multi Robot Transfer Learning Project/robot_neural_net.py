# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 23:20:17 2017

@author: peps
"""

#Details for the fully connected layer

#DOUBTS ::decide input shape dimension for first layer 

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
from keras.wrappers.scikit_learn import KerasRegressor

#state dimension ??
#feature map (??) , car_pos (X,Y,Z), car_orientation (alpha beta gamma), collision_distance ([2]), goal_pos (XYZ)


def getCompiledModel():
    model = Sequential()
    #input shape ?????????
    #number of hidden units -> 6
    model.add(Dense(4, kernel_initializer='normal', input_dim=7))  #-> works for both cumulated input and frame by frame input
    #model.add(Dense(11, kernel_initializer='lecun_uniform', input_shape=(1,11)))
    model.add(Activation('tanh'))
    #model.add(Dropout(0.2)) I'm not using dropout, but maybe you wanna give it a try?
    
    #model.add(Dense(1, kernel_initializer='lecun_uniform'))
    #model.add(Activation('relu'))
    #model.add(Dropout(0.2))
    
    #output size 5
    model.add(Dense(2, kernel_initializer='normal'))
    #model.add(Dense(2, kernel_initializer='lecun_uniform'))
    #model.add(Dense(4, init='lecun_uniform'))
    #model.add(Activation('softmax')) #linear output so we can have range of real-valued outputs
    
    #rms = RMSprop()
    model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['accuracy'])
    return model
    

def getOutput(state, model):
    action = model.predict(state, verbose = 1)
    #just to show an example output; read outputs left to right: up/down/left/right
    return action
