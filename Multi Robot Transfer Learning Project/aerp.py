# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 21:16:09 2017

@author: AdityaPMishra
"""
import numpy as np
import misc
import fc_neuralnet
import os
from keras.utils import np_utils
import pprint

model = misc.loadModel()
path = 'data\\test'
listing = os.listdir(path)
final_x_val = None
final_y_val = None
dFile1 = np.loadtxt(fname="leftVelocitysensor6.txt",dtype=np.float,delimiter=',')
dFile2 = np.loadtxt(fname="rightVelocitysensor6.txt",dtype=np.float,delimiter=',')
Finaldata = dFile2-dFile1
y_test=[]
    #print("hi")
for i in range(len(Finaldata)):
    if(Finaldata[i]<-1):
        y_test.append(0)
    if(Finaldata[i]<-0.25 and Finaldata[i]>=-1):
        y_test.append(1)
    if(Finaldata[i]<0 and Finaldata[i]>=-0.25):
        y_test.append(2)
    if(Finaldata[i]<0.25 and Finaldata[i]>=0):
        y_test.append(2)
    if(Finaldata[i]>=0.25 and Finaldata[i]<1):
        y_test.append(3)
    if(Finaldata[i]>=1):
        y_test.append(4)
#print(y_test)
y_test = np_utils.to_categorical(np.array(y_test), 5)
for infile1 in listing:
    print ("current file is: " + infile1)
    #get label from file name
    label = infile1[:1]
    print('label-->', label)
    #f = open('data\\train\\' + infile, 'r')
    x_val = np.load('data\\test\\' + infile1)
    #print('shape------->', x_train.shape[1])
    
    if final_x_val is None:    
        final_x_val = np.vstack(x_val)
    else:
        final_x_val = np.vstack((final_x_val, x_val))
    #get X_train array from file
    num_rows = len(x_val)

    #print('y_train->', y_val) 
    
print('model evaluation results-> ', model.evaluate(np.array([final_x_val[200]]), np.array([y_test[200]]), verbose=0, sample_weight=None))