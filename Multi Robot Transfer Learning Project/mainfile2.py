# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 11:11:03 2017

@author: AdityaPMishra
"""

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

import numpy as np
import misc
import fc_neuralnet
import os
from keras.utils import np_utils
import pprint
if __name__ == "__main__":
    #clientID = init.initEnv()
    
    
    model = misc.loadModel();
    print(model.summary())
    #collect data from files
    #loop over all the files
    #read each file-> get data-> feed data to neural network
    final_x_ar = None
    final_y_ar = None
    is_saved = 0
    path = 'data\\train'
    listing = os.listdir(path)
    dFile1 = np.loadtxt(fname="leftVelocitysensor01.txt",dtype=np.float,delimiter=',')
    dFile1 = np.append(dFile1,np.loadtxt(fname="leftVelocitysensor02.txt",dtype=np.float,delimiter=','))
    dFile1 = np.append(dFile1,np.loadtxt(fname="leftVelocitysensor03.txt",dtype=np.float,delimiter=','))
    #dFile1 = np.append(dFile1,np.loadtxt(fname="leftVelocitysensor04.txt",dtype=np.float,delimiter=','))
    #dFile1 = np.append(dFile1,np.loadtxt(fname="leftVelocitysensor5.txt",dtype=np.float,delimiter=','))
    dFile2 = np.loadtxt(fname="rightVelocitysensor01.txt",dtype=np.float,delimiter=',')
    dFile2 = np.append(dFile2,np.loadtxt(fname="rightVelocitysensor02.txt",dtype=np.float,delimiter=','))
    dFile2 = np.append(dFile2,np.loadtxt(fname="rightVelocitysensor03.txt",dtype=np.float,delimiter=','))
    #dFile2 = np.append(dFile2,np.loadtxt(fname="rightVelocitysensor04.txt",dtype=np.float,delimiter=','))
    #dFile2 = np.append(dFile2,np.loadtxt(fname="rightVelocitysensor5.txt",dtype=np.float,delimiter=','))
    #y_train = np.empty((num_rows, 3)) 
    #y_train.fill(int(label))
    #print('arr->', arr)
    #pprint.pprint(dFile1)
    #pprint.pprint(dFile2)
    Finaldata = dFile2-dFile1
    y_test=[]
    #print("hi")
    for i in range(0,len(Finaldata)-1):
        if(Finaldata[i+1]<-1):
            y_test.append(0)
        if(Finaldata[i+1]<-0.25 and Finaldata[i+1]>=-1):
            y_test.append(1)
        if(Finaldata[i+1]<0 and Finaldata[i+1]>=-0.25):
            y_test.append(2)
        if(Finaldata[i+1]<0.25 and Finaldata[i+1]>=0):
            y_test.append(2)
        if(Finaldata[i+1]>=0.25 and Finaldata[i+1]<1):
            y_test.append(3)
        if(Finaldata[i+1]>=1):
            y_test.append(4)
    #print(y_test)
    y_test.append(0)
    y_test = np_utils.to_categorical(np.array(y_test), 5)
    #print("here")
    #print(y_test)

    for infile in listing:
        arr = []
        print ("current file is: " + infile)
        #get label from file name
        #label = infile[:1]
        #label = int(label)
        #print('label-->', label)
        #f = open('data\\train\\' + infile, 'r')
        x_train = np.load('data\\train\\' + infile)
        #print('shape------->', x_train.shape[1])
        if final_x_ar is None:    
            final_x_ar = np.vstack(x_train)
        else:
            final_x_ar = np.vstack((final_x_ar, x_train))
        #get X_train array from file
        num_rows = len(x_train)
        #print('number of rows-->', num_rows)
        #initialize y_train array equal to size of x_train array

        
        #print('y_train->', y_train) 
    model.fit(final_x_ar, y_test, validation_split=0.25, epochs=10, verbose=1)
    misc.saveModel(model,"a") 
    
    #print(final_x_ar.shape[1])
