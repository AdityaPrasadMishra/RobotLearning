# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 03:42:07 2017

@author: peps
"""

import init
import sensor
import numpy as np
import misc
import time
import vrep

if __name__ == "__main__":
    clientID = init.initEnv()
   
    '''
    labels
    0-> straight
    1-> right
    2->left
    '''
    #label = 0
    #collect ( 1-9 ) sensor readings in an array and write them in a file
    #each sensor gives detected state, detected point and surface normal vector (7*9 = 63 feature vector)
    #output will be the intended direction of the vehicle (left, right, striaght)
    #print('getting sensor readings')
    #sensor_arr = sensor.getAllSensorReadings(13.3)
    #code, sensor3 = sensor.getHandle('sensor3')
    #code, sensor4 = sensor.getHandle('sensor4')
    readings = []
    leftVelocityarray =[]
    rightVelocityarray =[]
    errorcode,sensor1 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor1',vrep.simx_opmode_oneshot_wait)
    #print('handle--> ', sensor1 , ' errorcode-->', errorcode)
    errorcode,sensor2 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor2',vrep.simx_opmode_oneshot_wait)
    #print('handle--> ', sensor2 , ' errorcode-->', errorcode)
    errorcode,sensor3 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor3',vrep.simx_opmode_oneshot_wait)
    #print('handle--> ', sensor3 , ' errorcode-->', errorcode)
    errorcode,sensor4 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor4',vrep.simx_opmode_oneshot_wait)
    #print('handle--> ', sensor4 , ' errorcode-->', errorcode)
    errorcode,sensor5 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor5',vrep.simx_opmode_oneshot_wait)
    #print('handle--> ', sensor5, ' errorcode-->', errorcode)
    errorcode,sensor6 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor6',vrep.simx_opmode_oneshot_wait)
    #print('handle--> ', sensor6 , ' errorcode-->', errorcode)
    errorcode,sensor7 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor7',vrep.simx_opmode_oneshot_wait)
    #print('handle--> ', sensor7, ' errorcode-->', errorcode)
    errorcode,sensor8 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor8',vrep.simx_opmode_oneshot_wait)
    #print('handle--> ', sensor8, ' errorcode-->', errorcode)
    errorcode,sensor9 = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor9',vrep.simx_opmode_oneshot_wait)
    print('handle--> ', sensor9, ' errorcode-->', errorcode)
    errorcode,leftMotorhandle = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_oneshot_wait)
    errorcode,rightMotorhandle = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_oneshot_wait)
    returnCode,leftlinearVelocity=vrep.simxGetObjectFloatParameter(clientID,leftMotorhandle,2012,vrep.simx_opmode_streaming)
    returnCode,rightlinearVelocity=vrep.simxGetObjectFloatParameter(clientID,rightMotorhandle,2012,vrep.simx_opmode_streaming)
    
    startTime=time.time()
    sensor_errorcode, detectionState1, detectedPoint1, detectedObjHandle1, detectedSurfaceNormalVector1 = vrep.simxReadProximitySensor (clientID,sensor1,vrep.simx_opmode_streaming)
    sensor_errorcode, detectionState2, detectedPoint2, detectedObjHandle2, detectedSurfaceNormalVector2 = vrep.simxReadProximitySensor (clientID,sensor2,vrep.simx_opmode_streaming)
    sensor_errorcode, detectionState3, detectedPoint3, detectedObjHandle3, detectedSurfaceNormalVector3 = vrep.simxReadProximitySensor (clientID,sensor3,vrep.simx_opmode_streaming)
    sensor_errorcode, detectionState4, detectedPoint4, detectedObjHandle4, detectedSurfaceNormalVector4 = vrep.simxReadProximitySensor (clientID,sensor4,vrep.simx_opmode_streaming)
    sensor_errorcode, detectionState5, detectedPoint5, detectedObjHandle5, detectedSurfaceNormalVector5 = vrep.simxReadProximitySensor (clientID,sensor5,vrep.simx_opmode_streaming)
    sensor_errorcode, detectionState6, detectedPoint6, detectedObjHandle6, detectedSurfaceNormalVector6 = vrep.simxReadProximitySensor (clientID,sensor6,vrep.simx_opmode_streaming)
    sensor_errorcode, detectionState7, detectedPoint7, detectedObjHandle7, detectedSurfaceNormalVector7 = vrep.simxReadProximitySensor (clientID,sensor7,vrep.simx_opmode_streaming)
    sensor_errorcode, detectionState8, detectedPoint8, detectedObjHandle8, detectedSurfaceNormalVector8 = vrep.simxReadProximitySensor (clientID,sensor8,vrep.simx_opmode_streaming) 
    sensor_errorcode, detectionState9, detectedPoint9, detectedObjHandle9, detectedSurfaceNormalVector9 = vrep.simxReadProximitySensor (clientID,sensor9,vrep.simx_opmode_streaming)
   
    while time.time()-startTime < 20:  
        #print(time.time()-startTime)
        
        row = []
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
        returnCode,leftlinearVelocity=vrep.simxGetObjectFloatParameter(clientID,leftMotorhandle,2012,vrep.simx_opmode_buffer)
        returnCode,rightlinearVelocity=vrep.simxGetObjectFloatParameter(clientID,rightMotorhandle,2012,vrep.simx_opmode_buffer)
        leftVelocityarray.append(leftlinearVelocity)
        rightVelocityarray.append(rightlinearVelocity)
       
        #print(row)
        row = (np.hstack(row))
        readings.append(row)
    readings = np.array(readings)
    #write the array to file along with the label
    #ar = [[1,2,3,4], [2,3,4,5], [3,4,5,6], [4,5,6,7]]
    #print ('array -->', ar)
    #all_data = np.hstack((ar, 10))
    #print('all data->', readings)
    #print(leftVelocityarray)
    #print(rightVelocityarray)
    leftVelocityarray = np.array(leftVelocityarray)
    rightVelocityarray = np.array(rightVelocityarray)
    print(len(readings))
    print(len(leftVelocityarray)) 
    print('writing to file')
    filename = 'sensorFile_' + str(time.time())
    with open('leftVelocitysensor04.txt','wb') as f:
        np.savetxt('leftVelocitysensor04.txt',leftVelocityarray[None, :],'%f',delimiter=',')
    with open('rightVelocitysensor04.txt','wb') as f:
        np.savetxt('rightVelocitysensor04.txt',rightVelocityarray[None, :],'%f',delimiter=',')
    misc.writeToFile(readings, filename)
    
    
    #train the task neural network
    
    
    '''list1 = []
    list2 = [1,2,3,4,5,6,7,8,9]
    list1.append(list2)
    
    list3 = [2,3,4,5,6,7,8,9,10]
    list1.append(list3)
    
    print (np.array(list1))'''