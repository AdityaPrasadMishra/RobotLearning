# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 07:11:53 2017

@author: peps
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 03:42:07 2017

@author: peps
"""

#train robot specific neural network


import numpy as np
import misc
import robot_neural_net
import os
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

def column(matrix, i):
    return [row[i] for row in matrix]


if __name__ == "__main__":
    #clientID = init.initEnv()
    
    
    model = robot_neural_net.getCompiledModel();
    print(model.summary())
    #collect data from files
    #loop over all the files
    #read each file-> get data-> feed data to neural network
    final_ar = None
    final_x_ar = None
    final_y_ar = None
    is_saved = 0
    path = 'data\\train'
    listing = os.listdir(path)
    total_lines = 0
    for infile in listing:
        arr = []
        print ("current file is: " + infile)
        #get label from file name
        label = infile[:1]
        label = int(label)
        print('label-->', label)
        #f = open('data\\train\\' + infile, 'r')
        x_train = np.load('data\\train\\' + infile)
        print('shape------->', x_train.shape)
        total_lines+=x_train.shape[0]
        print('lines-->', total_lines)
        
        if final_ar is None:    
            final_ar = np.vstack(x_train)
            print('truncated array shape-->', final_ar.shape[1])
        else:
            final_ar = np.vstack((final_ar, x_train))
        #get X_train array from file
        num_rows = len(x_train)
    
    #print(column(final_ar, 7))
    leftspeed_ar = np.array(column(final_ar, 7))
    rightspeed_ar = np.array(column(final_ar, 8))
    leftspeed_ar = leftspeed_ar.reshape(len(leftspeed_ar), 1)
    rightspeed_ar = rightspeed_ar.reshape(len(leftspeed_ar), 1)
    
    new_left_ar = []
    for row in leftspeed_ar:
        row = np.hstack(row)
        new_left_ar.append(row)
    
    new_left_ar = np.array(new_left_ar)
    
    new_right_ar = []
    for row in rightspeed_ar:
        row = np.hstack(row)
        new_right_ar.append(row)
    
    new_right_ar = np.array(new_right_ar)
    print('left array ->', new_left_ar.shape)
    print('right array ->', new_right_ar.shape)
    
    print(new_left_ar)
    #print(new_right_ar)

    final_y_ar = []
    for i in range(len(leftspeed_ar)):
        final_row = []
        final_row.append(new_left_ar[i][0])
        final_row.append(new_right_ar[i][0])
        final_y_ar.append(final_row)
        
    final_y_ar = np.array(final_y_ar)
    print(final_y_ar.shape)
        
    final_x_ar = np.delete(final_ar, np.s_[7:9], axis=1)
    
    seed = 7
    np.random.seed(seed)
    model.fit(final_x_ar, final_y_ar, validation_split = 0.25, epochs=100, verbose=1)

    # evaluate model with standardized dataset
    #estimator = KerasRegressor(build_fn=model, nb_epoch=100, batch_size=5, verbose=0)
    #kfold = KFold(n_splits=10, random_state=seed)
    #results = cross_val_score(estimator, final_x_ar, final_y_ar, cv=kfold)
    #print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))
    misc.saveModel(model,1)

    final_y_test = None
    final_test = None
    final_x_test = None
    print('predicting data')
    model = misc.loadModel(1)
    
    path = 'data\\test1'
    listing = os.listdir(path)
    for infile2 in listing:
        print ("current file is: " + infile2)
      
        x_test = np.load('data\\test1\\' + infile2)
        
        
        if final_test is None:    
            final_test = np.vstack(x_test)
            print('truncated array shape-->', final_test.shape[1])
        else:
            final_test = np.vstack((final_test, x_test))
        #get X_train array from file
        num_rows = len(x_test)
    
     
    #print(column(final_ar, 7))
    leftspeed_ar = np.array(column(final_test, 7))
    rightspeed_ar = np.array(column(final_test, 8))
    leftspeed_ar = leftspeed_ar.reshape(len(leftspeed_ar), 1)
    rightspeed_ar = rightspeed_ar.reshape(len(leftspeed_ar), 1)
    
    new_left_ar = []
    for row in leftspeed_ar:
        row = np.hstack(row)
        new_left_ar.append(row)
    
    new_left_ar = np.array(new_left_ar)
    
    new_right_ar = []
    for row in rightspeed_ar:
        row = np.hstack(row)
        new_right_ar.append(row)
    
    new_right_ar = np.array(new_right_ar)
    print('left array ->', new_left_ar.shape)
    print('right array ->', new_right_ar.shape)
    
    print(new_left_ar)
    #print(new_right_ar)

    final_y_test = []
    for i in range(len(new_right_ar)):
        final_row = []
        final_row.append(new_left_ar[i][0])
        final_row.append(new_right_ar[i][0])
        final_y_test.append(final_row)
        
    final_y_test = np.array(final_y_test)
    print(final_y_test.shape)
        
    final_x_test = np.delete(final_test, np.s_[7:9], axis=1)
       
    print(model.evaluate(final_x_test, final_y_test, verbose=1))
    print(model.predict(final_x_test[0].reshape(1,7)))
    print(final_y_test[0])