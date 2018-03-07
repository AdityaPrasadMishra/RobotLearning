# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 12:01:51 2017

@author: AdityaPMishra
"""

import numpy as np
import random
import vrep
import sys
import time   
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
K.set_image_dim_ordering('th')
from matplotlib import pyplot
from scipy.misc import toimage
import scipy.stats as st
import matplotlib.image as mp
import argparse
from keras.callbacks import ModelCheckpoint
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.layers import Lambda,Activation, Flatten, Dense, Dropout
from keras.layers.normalization import BatchNormalization

model = load_model("model-006.h5")
print ('Program started')
vrep.simxFinish(-1) 
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) 
if clientID!=-1:
    imagearray=[]
    leftVelocityarray =[]
    rightVelocityarray =[]
    print ('Connected to remote API server')

    res,objs=vrep.simxGetObjects(clientID,vrep.sim_handle_all,vrep.simx_opmode_oneshot_wait)
    errorcode,cam_Handle = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_vision_sensor',vrep.simx_opmode_oneshot_wait)
    returnCode,data=vrep.simxGetIntegerParameter(clientID,vrep.sim_intparam_mouse_x,vrep.simx_opmode_streaming) 
    errorcode,leftMotorhandle = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_oneshot_wait)
    errorcode,rightMotorhandle = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_oneshot_wait)
    errorcode,ultrasonicSensor3handle = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor3',vrep.simx_opmode_oneshot_wait)
    errorcode,ultrasonicSensor4handle = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor4',vrep.simx_opmode_oneshot_wait)
    errorcode,p3dx_Goalhandle = vrep.simxGetObjectHandle(clientID,'p3dx_Goal',vrep.simx_opmode_oneshot_wait)
    returnCode,linearVelocity=vrep.simxGetObjectFloatParameter(clientID,leftMotorhandle,2012,vrep.simx_opmode_streaming)
    returnCode,linearVelocity=vrep.simxGetObjectFloatParameter(clientID,rightMotorhandle,2012,vrep.simx_opmode_streaming)

    if res==vrep.simx_return_ok:
        print ('Number of objects in the scene: ',len(objs))
    else:
        print ('Remote API function call returned with error code: ',res)

    time.sleep(2)
   
    startTime=time.time()   
    vrep.simxGetIntegerParameter(clientID,vrep.sim_intparam_mouse_x,vrep.simx_opmode_streaming) 
    ireturnCode,resolution,image=vrep.simxGetVisionSensorImage(clientID,cam_Handle,0,vrep.simx_opmode_streaming)
    i=0
    while time.time()-startTime < 70:   
        #print(time.time())
        ireturnCode,resolution,image=vrep.simxGetVisionSensorImage(clientID,cam_Handle,0,vrep.simx_opmode_buffer)
        if ireturnCode==vrep.simx_return_ok:
            image = np.array(image)
            image.resize(128,128,3)
            image.resize(3,128,128)
            image = image.astype('float32')
            image = image/255.0
            image = np.expand_dims(image, axis=0)
            y = model.predict(image)
            ynew=y[0][0]
            relvel=0
            if(y==0):
                relvel=-1
            elif(ynew>0 and ynew<1):
                relvel = -0.25
            elif(y>=1 and ynew<2):
                relvel = 0
            elif(ynew>=2 and ynew<3):
                relvel = 0.25
            elif(ynew>=3 and ynew<4):
                relvel = 1
            
            returnCode=vrep.simxSetJointTargetVelocity(clientID,rightMotorhandle,3,vrep.simx_opmode_streaming)
            returnCode=vrep.simxSetJointTargetVelocity(clientID,leftMotorhandle,3-relvel,vrep.simx_opmode_streaming)
            #print(y)
            #print(image.shape)
            #print(image)
            #print(image.shape)
            
            print(y)
            #inp.resize([resolution[0],resolution[1],3])
            #plt.imshow(inp,origin="lower")

    vrep.simxAddStatusbarMessage(clientID,'Hello V-REP!',vrep.simx_opmode_oneshot)
    
    vrep.simxGetPingTime(clientID)
else:
    print('Connection unsuccessful')
    sys.exit('Could not Connect')
