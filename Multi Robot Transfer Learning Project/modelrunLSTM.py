# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 03:25:17 2017

@author: AdityaPMishra
"""

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
import PIL

model1 = load_model("model-006.h5")
print ('Program started')
vrep.simxFinish(-1) 
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) 
if clientID!=-1:
    imagearray=[]
    leftVelocityarray =[]
    rightVelocityarray =[]
    print ('Connected to remote API server')
    model = misc.loadModel()
     
    #car handle
    errorcode, car_handle = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx',vrep.simx_opmode_oneshot_wait)
   
    #sensors handles
    errorcode,sensor1 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor1',vrep.simx_opmode_oneshot_wait)
    print('handle--> ', sensor1 , ' errorcode-->', errorcode)
    errorcode,sensor2 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor2',vrep.simx_opmode_oneshot_wait)
    print('handle--> ', sensor2 , ' errorcode-->', errorcode)
    errorcode,sensor3 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor3',vrep.simx_opmode_oneshot_wait)
    print('handle--> ', sensor3 , ' errorcode-->', errorcode)
    errorcode,sensor4 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor4',vrep.simx_opmode_oneshot_wait)
    print('handle--> ', sensor4 , ' errorcode-->', errorcode)
    errorcode,sensor5 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor5',vrep.simx_opmode_oneshot_wait)
    print('handle--> ', sensor5, ' errorcode-->', errorcode)
    errorcode,sensor6 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor6',vrep.simx_opmode_oneshot_wait)
    print('handle--> ', sensor6 , ' errorcode-->', errorcode)
    errorcode,sensor7 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor7',vrep.simx_opmode_oneshot_wait)
    print('handle--> ', sensor7, ' errorcode-->', errorcode)
    errorcode,sensor8 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor8',vrep.simx_opmode_oneshot_wait)
    print('handle--> ', sensor8, ' errorcode-->', errorcode)
    errorcode,sensor9 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor9',vrep.simx_opmode_oneshot_wait)
    print('handle--> ', sensor9, ' errorcode-->', errorcode)
    
    errorcode,leftMotorhandle = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_oneshot_wait)
    errorcode,rightMotorhandle = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_oneshot_wait)
      
    readings = []
    
    startTime=time.time()
    
    #car position and orientation readings
    errorcode, car_position = vrep.simxGetObjectPosition(clientID,car_handle,-1,vrep.simx_opmode_streaming)
    errorcode, car_orientation = vrep.simxGetObjectOrientation(clientID,car_handle,-1,vrep.simx_opmode_streaming)
    
    returnCode,leftlinearVelocity=vrep.simxGetObjectFloatParameter(clientID,leftMotorhandle,2012,vrep.simx_opmode_streaming)
    returnCode,rightlinearVelocity=vrep.simxGetObjectFloatParameter(clientID,rightMotorhandle,2012,vrep.simx_opmode_streaming)
    
    #get sensor readings
    sensor_errorcode, detectionState1, detectedPoint1, detectedObjHandle1, detectedSurfaceNormalVector1 = vrep.simxReadProximitySensor (clientID,sensor1,vrep.simx_opmode_streaming)
    sensor_errorcode, detectionState2, detectedPoint2, detectedObjHandle2, detectedSurfaceNormalVector2 = vrep.simxReadProximitySensor (clientID,sensor2,vrep.simx_opmode_streaming)
    sensor_errorcode, detectionState3, detectedPoint3, detectedObjHandle3, detectedSurfaceNormalVector3 = vrep.simxReadProximitySensor (clientID,sensor3,vrep.simx_opmode_streaming)
    sensor_errorcode, detectionState4, detectedPoint4, detectedObjHandle4, detectedSurfaceNormalVector4 = vrep.simxReadProximitySensor (clientID,sensor4,vrep.simx_opmode_streaming)
    sensor_errorcode, detectionState5, detectedPoint5, detectedObjHandle5, detectedSurfaceNormalVector5 = vrep.simxReadProximitySensor (clientID,sensor5,vrep.simx_opmode_streaming)
    sensor_errorcode, detectionState6, detectedPoint6, detectedObjHandle6, detectedSurfaceNormalVector6 = vrep.simxReadProximitySensor (clientID,sensor6,vrep.simx_opmode_streaming)
    sensor_errorcode, detectionState7, detectedPoint7, detectedObjHandle7, detectedSurfaceNormalVector7 = vrep.simxReadProximitySensor (clientID,sensor7,vrep.simx_opmode_streaming)
    sensor_errorcode, detectionState8, detectedPoint8, detectedObjHandle8, detectedSurfaceNormalVector8 = vrep.simxReadProximitySensor (clientID,sensor8,vrep.simx_opmode_streaming) 
    sensor_errorcode, detectionState9, detectedPoint9, detectedObjHandle9, detectedSurfaceNormalVector9 = vrep.simxReadProximitySensor (clientID,sensor9,vrep.simx_opmode_streaming)

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
    k=0
    images =[]
    while time.time()-startTime < 70:   
        #print(time.time())
        #k=k+1
        row = []
        robot_row = []
        
        ireturnCode,resolution,image=vrep.simxGetVisionSensorImage(clientID,cam_Handle,0,vrep.simx_opmode_buffer)
        if ireturnCode==vrep.simx_return_ok:
            #print("in here")
            #print(image)
            k=k+1
            #print("k in="+str(k))            
            if k>5:
                if k%2==0:
                        #input for task module
                    sensor_errorcode, detectionState1, detectedPoint1, detectedObjHandle1, detectedSurfaceNormalVector1 = vrep.simxReadProximitySensor (clientID,sensor1,vrep.simx_opmode_buffer)
                    row.append(detectionState1)
                    row.append(detectedPoint1)
                    row.append(detectedSurfaceNormalVector1)
                    sensor_errorcode, detectionState2, detectedPoint2, detectedObjHandle2, detectedSurfaceNormalVector2 = vrep.simxReadProximitySensor (clientID,sensor2,vrep.simx_opmode_buffer)
                    row.append(detectionState2)
                    row.append(detectedPoint2)
                    row.append(detectedSurfaceNormalVector2)
                    sensor_errorcode, detectionState3, detectedPoint3, detectedObjHandle3, detectedSurfaceNormalVector3 = vrep.simxReadProximitySensor (clientID,sensor3,vrep.simx_opmode_buffer)
                    row.append(detectionState3)
                    row.append(detectedPoint3)
                    row.append(detectedSurfaceNormalVector3)
                    sensor_errorcode, detectionState4, detectedPoint4, detectedObjHandle4, detectedSurfaceNormalVector4 = vrep.simxReadProximitySensor (clientID,sensor4,vrep.simx_opmode_buffer)
                    row.append(detectionState4)
                    row.append(detectedPoint4)
                    row.append(detectedSurfaceNormalVector4)
                    sensor_errorcode, detectionState5, detectedPoint5, detectedObjHandle5, detectedSurfaceNormalVector5 = vrep.simxReadProximitySensor (clientID,sensor5,vrep.simx_opmode_buffer)
                    row.append(detectionState5)
                    row.append(detectedPoint5)
                    row.append(detectedSurfaceNormalVector5)
                    sensor_errorcode, detectionState6, detectedPoint6, detectedObjHandle6, detectedSurfaceNormalVector6 = vrep.simxReadProximitySensor (clientID,sensor6,vrep.simx_opmode_buffer)
                    row.append(detectionState6)
                    row.append(detectedPoint6)
                    row.append(detectedSurfaceNormalVector6)
                    sensor_errorcode, detectionState7, detectedPoint7, detectedObjHandle7, detectedSurfaceNormalVector7 = vrep.simxReadProximitySensor (clientID,sensor7,vrep.simx_opmode_buffer)
                    row.append(detectionState7)
                    row.append(detectedPoint7)
                    row.append(detectedSurfaceNormalVector7)
                    sensor_errorcode, detectionState8, detectedPoint8, detectedObjHandle8, detectedSurfaceNormalVector8 = vrep.simxReadProximitySensor (clientID,sensor8,vrep.simx_opmode_buffer) 
                    row.append(detectionState8)
                    row.append(detectedPoint8)
                    row.append(detectedSurfaceNormalVector8)
                    sensor_errorcode, detectionState9, detectedPoint9, detectedObjHandle9, detectedSurfaceNormalVector9 = vrep.simxReadProximitySensor (clientID,sensor9,vrep.simx_opmode_buffer)
                    row.append(detectionState9)
                    row.append(detectedPoint9)
                    row.append(detectedSurfaceNormalVector9)
                    
                    print('row->', row)
                    print('original row shape-->', len(row))
                    
                    #modify the row ipnut
                    row = (np.hstack(row))
                    #row = (sparse.hstack(row))
                    #row = row.reshape(1,63)
                    #print('new row-->', new_row)
                    #new_row = np.zeros((1, 63))
                    #row = row.reshape(1,63)
                    print('data shape-->', row.shape)
                    
                    rowtrans = np.reshape(row,(1,63))
                    print(len(images))
                    for mk in range(4):
                        
                        print(mk)
                        images[mk] = images[mk+1]
                        image = np.array(image,dtype=np.uint8)
                        image.resize([128,128,3])
                        #print(image)
                        image = np.array(image)
                        image = PIL.Image.fromarray(image)
                        image = image.resize((40,40), PIL.Image.ANTIALIAS)
                        #image.resize(128,128,3)
                        #image.resize(3,40,40)
                        image = np.array(image)
                        image.resize(3,40,40)
                        image = image.astype('float32')
                        image = image/255.0
                        images[4] = image
                    images1 = np.expand_dims(images, axis=0)
                    #print(np.array(images).shape)
                    directional_speed = np.argmax(model1.predict(images1))
                    #print(np.argmax(y))
                    #ynew=y[0][0]
                    
                    #print("directional speed_ar :", directional_speed_ar)
                    #directional_speed = directional_speed_ar.index(max(directional_speed_ar))
                    print("directional speed :", directional_speed)
                    #mock input
                    #directional_speed = 3
                    robot_row.append(directional_speed)
                    
                    #get car orientation and car position
                    errorcode, car_position = vrep.simxGetObjectPosition(clientID,car_handle,-1,vrep.simx_opmode_buffer)
                    robot_row.append(car_position)
                    
                    errorcode, car_orientation = vrep.simxGetObjectOrientation(clientID,car_handle,-1,vrep.simx_opmode_buffer)
                    robot_row.append(car_orientation)
                    
                    #get car velocities
                    returnCode,leftlinearVelocity=vrep.simxGetObjectFloatParameter(clientID,leftMotorhandle,2012,vrep.simx_opmode_buffer)
                    robot_row.append(leftlinearVelocity)
                    
                    returnCode,rightlinearVelocity=vrep.simxGetObjectFloatParameter(clientID,rightMotorhandle,2012,vrep.simx_opmode_buffer)
                    robot_row.append(rightlinearVelocity)    
                
                    print(robot_row)
                    robot_row = (np.hstack(robot_row))
                    readings.append(robot_row)
                #print(y)
                        #print(image.shape)
                        #print(image)
                        #print(image.shape)
                        
                        
                        #print(y)
                        #inp.resize([resolution[0],resolution[1],3])
                        #plt.imshow(inp,origin="lower")
                    
            else:
                print("k="+str(k))
                #ireturnCode,resolution,image=vrep.simxGetVisionSensorImage(clientID,cam_Handle,0,vrep.simx_opmode_buffer)
                #if ireturnCode==vrep.simx_return_ok:    
                    #print(resolution)
                    #print(ireturnCode)
                #print(image)
                image = np.array(image,dtype=np.uint8)
                image.resize([128,128,3])
                #print(image)
                image = np.array(image)
                image = PIL.Image.fromarray(image)
                image = image.resize((40,40), PIL.Image.ANTIALIAS)
     #               image.resize(128,128,3)                
                image = np.array(image)
                image.resize(3,40,40)
                image = image.astype('float32')
                image = image/255.0
                images.append(image)
            
            
            

    vrep.simxAddStatusbarMessage(clientID,'Hello V-REP!',vrep.simx_opmode_oneshot)
    
    vrep.simxGetPingTime(clientID)
    readings = np.array(readings)
    #write the array to file along with the label
    #ar = [[1,2,3,4], [2,3,4,5], [3,4,5,6], [4,5,6,7]]
    #print ('array -->', ar)
    #all_data = np.hstack((ar, 10))
    #print('all data->', readings)
    
    print('writing to file')
    filename = str(label) + '_sensor_' + str(time.time())
    misc.writeToFile(readings, filename)
else:
    print('Connection unsuccessful')
    sys.exit('Could not Connect')
