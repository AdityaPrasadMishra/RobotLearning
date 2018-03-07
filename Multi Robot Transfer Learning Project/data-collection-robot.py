# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 03:42:07 2017

@author: peps
"""

import init
import numpy as np
import misc
import time
import vrep
import fc_neuralnet
from scipy import sparse

if __name__ == "__main__":
    clientID = init.initEnv()
   
    '''
    labels
    0-> 
    1-> 
    2->
    3->
    4->
    '''
    label = 0
    
    #relate throttle with steering angle
    #output from task modue -> direction
    #lesser difference between the left and right motor speeds, greater the velocity should be
    
    #collect robot controls readings in an array and write them in a file
    #(position, speed, orientation)
    #position,  length -> (3)
    #orientation,  length -> (3)
    #(speed difference obtained from task specific module)(direction), length-> (1)
    #total feature vector length ->(7)
    #output will be the speeds of the vehicle (speed) (length) -> (2)
    
    
    #load saved model from disk
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
    
    while time.time()-startTime < 30:        
        row = []
        robot_row = []
        
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
        #get output from task module
        #directional_speed_ar = list(fc_neuralnet.getOutput(rowtrans, model))
        directional_speed_ar = fc_neuralnet.getOutput(rowtrans, model)
        directional_speed = np.argmax(directional_speed_ar)
        print("directional speed_ar :", directional_speed_ar)
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
    
    readings = np.array(readings)
    #write the array to file along with the label
    #ar = [[1,2,3,4], [2,3,4,5], [3,4,5,6], [4,5,6,7]]
    #print ('array -->', ar)
    #all_data = np.hstack((ar, 10))
    #print('all data->', readings)
    
    print('writing to file')
    filename = str(label) + '_sensor_' + str(time.time())
    misc.writeToFile(readings, filename)
        
    #train the task neural network
    
    
    '''list1 = []
    list2 = [1,2,3,4,5,6,7,8,9]
    list1.append(list2)
    
    list3 = [2,3,4,5,6,7,8,9,10]
    list1.append(list3)
    
    print (np.array(list1))'''