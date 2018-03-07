# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 22:26:32 2017

@author: peps
"""
import numpy as np
import time
import os, errno
from keras.models import model_from_json
from keras.optimizers import RMSprop
from keras.models import Sequential
from keras.layers import Dense


goal_pos = [[-6.5445e+00, -2.4140e-06, +1.3879e-01], []]

'''def getLastCreatedFile(directory):
    for filename in os.listdir(directory):
    if filename.endswith(".json"): 
        # print(os.path.join(directory, filename))
        continue
    else:
        continue'''

def formatInp(inp):
    #print('input-->', inp)
    out = (np.hstack(inp))
    #print ('formatted out-->', out)
    return out

def generateArrays(X):
    X_train = X[:int(2*len(X)/3)]
    X_test= X[int(len(X_train)):]
    
    return np.array(X_train), np.array(X_test)


#misc functions 
def formatData(data):
    #print('data-->', data)
    length = len(data)
    #final = [[] for x in range(length)]
    new = [[] for x in range(length)]
    
    '''for i in range(0, len(data)):
        format_state = formatInp(data[i])
        final[i] = format_state
    
    #print('final-->', final)
    
    for i in range(0, len(final)):
        for j in range(0, len(final[i])):
            print(final[i][j])
            new[i].append(final[i][j])
            print(new[i])'''
    new = formatInp(data)
    #print('new-->', new)        
    return new

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

def saveModel(model):       
    # serialize model to JSON
    #cur_time_str = str(time.time())
    model_json = model.to_json()
    
    #if file exists, remove
    silentremove("model.json")
    silentremove("model.h5")
    
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
        # serialize weights to HDF5
    model.save_weights("model.h5")
    print("Saved model to disk") 

def saveModel(model,x):       
    # serialize model to JSON
    #cur_time_str = str(time.time())
    model_json = model.to_json()
    
    #if file exists, remove
    silentremove("model_"+x+".json")
    silentremove("model_"+x+"h5")
    
    with open("model1.json", "w") as json_file:
        json_file.write(model_json)
        # serialize weights to HDF5
    model.save_weights("model1.h5")
    print("Saved model to disk")

def loadModel(name_str = None):
    #look up last saved model and weights
    if name_str is None:
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("model.h5")
        
        #rms = RMSprop()
        loaded_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    else:
        json_file = open(name_str+".json", 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(name_str+".h5")
        
        #rms = RMSprop()
        loaded_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return loaded_model
  
def writeToFile(arr, filename):
    np.save(filename, arr)
    