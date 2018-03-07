# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import vrep
import time
import math
#from learning import cnn
import numpy as np

clientID = -1

def setClient(cID):
   global clientID
   clientID = cID

def getHandle(str):
    if str == 'vision':
        #get handle for vision sensor
        errorcode,handle = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_vision_sensor',vrep.simx_opmode_oneshot_wait)
        return errorcode, handle
    
    elif str == 'car':
        #get handle for car    
        errorcode, handle = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx',vrep.simx_opmode_oneshot_wait)
        return errorcode, handle
    
    elif str == 'left':
        #get handle for left motor    
        errorcode,handle = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_oneshot_wait)
        return errorcode, handle
    
    elif str == 'right':
        #get handle for right motor
        errorcode,handle = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_oneshot_wait)
        return errorcode, handle
    
    
    elif 'sensor' in str:
         print('str last character-->', str[-1])
         errorcode,handle = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor' + str[-1],vrep.simx_opmode_oneshot_wait)
         print('handle--> ', handle , ' errorcode-->', errorcode)
         return errorcode, handle

         
    elif str == 'goal':
        #get handle for goal
        errorcode,handle = vrep.simxGetObjectHandle(clientID,'p3dx_Goal',vrep.simx_opmode_oneshot_wait)
        return errorcode, handle


def getCurPosition():
    print('get current position')
    
    code, car_handle = getHandle('car')
    #print('car_handle-->', car_handle)
    #get car position
    errorcode, car_position = vrep.simxGetObjectPosition(clientID,car_handle,-1,vrep.simx_opmode_streaming)
    startTime=time.time() 
    while time.time()-startTime < 1:   
        ireturnCode,car_position=vrep.simxGetObjectPosition(clientID,car_handle,-1,vrep.simx_opmode_buffer)
        #if ireturnCode==vrep.simx_return_ok:
            #print (car_position)
    return car_position
 
    
def getCurOrientation():
    print('get current orientation')
    
    code, car_handle = getHandle('car')
    
    #get car orientation
    errorcode, car_orientation = vrep.simxGetObjectOrientation(clientID,car_handle,-1,vrep.simx_opmode_streaming)
    startTime=time.time() 
    while time.time()-startTime < 1:   
        ireturnCode, car_angle = vrep.simxGetObjectOrientation(clientID,car_handle,-1,vrep.simx_opmode_buffer)
        #if ireturnCode==vrep.simx_return_ok:
        #    print (car_angle)
    return car_angle

def getCurrentImage():
    print('get current image')
    
    code, vision_sensor_handle = getHandle('vision')
    
    startTime=time.time()    
    ireturnCode,resolution,image=vrep.simxGetVisionSensorImage(clientID,vision_sensor_handle,0,vrep.simx_opmode_streaming)
    while time.time()-startTime < 1:   
        ireturnCode,resolution,image=vrep.simxGetVisionSensorImage(clientID,vision_sensor_handle,0,vrep.simx_opmode_buffer) 
        #if ireturnCode==vrep.simx_return_ok:
        #    print (image)
    return image

def getCurrentImageContinuous():
    
    imagearray=[]
    print('get current image from vision sensor in continuos mode')
    
    code, vision_sensor_handle = getHandle('vision')
    startTime=time.time()   
    i=0
    ireturnCode,resolution,image=vrep.simxGetVisionSensorImage(clientID,vision_sensor_handle,0,vrep.simx_opmode_streaming)
    while time.time()-startTime < 15:   
        ireturnCode,resolution,image=vrep.simxGetVisionSensorImage(clientID,vision_sensor_handle,0,vrep.simx_opmode_buffer) 
        if ireturnCode==vrep.simx_return_ok:
            i=i+1
            inp = np.array(image, dtype=np.uint8)
            imagearray.append(inp)
            #print (image)
    imagearray = np.array(imagearray)
    return imagearray
    

def setJointVelocity(speeds):
    print('setting velocity for both motors')
    
    code, left_handle = getHandle('left')
    code, right_handle = getHandle('right')
    
    left_return_code = vrep.simxSetJointTargetVelocity(clientID, left_handle, speeds[0], vrep.simx_opmode_oneshot_wait)
    right_return_code = vrep.simxSetJointTargetVelocity(clientID, right_handle, speeds[0], vrep.simx_opmode_oneshot_wait)
    
    return [left_return_code, right_return_code]
    
def getCollisionDistance():
    print('getting collision distances')
    #more sensors to be added later on 
    
    
    code, sensor3 = getHandle('sensor3')
    code, sensor4 = getHandle('sensor4')
    
    startTime=time.time()
    #get proximity sensor3 readings 
    sensor_errorcode, detectionState, detectedPoint, detectedObjHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor (clientID,sensor3,vrep.simx_opmode_streaming)
    
    #get proximity sensor4 readings 
    sensor_errorcode, detectionState, detectedPoint, detectedObjHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor (clientID,sensor4,vrep.simx_opmode_streaming)
    
    while time.time()-startTime < 1:   
         #get proximity sensor3 readings 
         sensor_errorcode_3, detectionState_3, detectedPoint, detectedObjHandle, detectedSurfaceNormalVector_3 = vrep.simxReadProximitySensor (clientID,sensor3,vrep.simx_opmode_buffer)
    
         #get proximity sensor4 readings 
         sensor_errorcode_4, detectionState_4, detectedPoint, detectedObjHandle, detectedSurfaceNormalVector_4 = vrep.simxReadProximitySensor (clientID,sensor4,vrep.simx_opmode_buffer) 
         #if sensor_errorcode_4 == vrep.simx_return_ok and sensor_errorcode_3 == vrep.simx_return_ok:
         #    print(detectedSurfaceNormalVector_3 + ',' + detectedSurfaceNormalVector_4)
         
    #distance3 = math.sqrt((detectedSurfaceNormalVector_3[0]**2) + (detectedSurfaceNormalVector_3[1]**2))
    #distance4 = math.sqrt((detectedSurfaceNormalVector_4[0]**2) + (detectedSurfaceNormalVector_4[1]**2))
    
    
    #return [distance3, distance4]
    return [detectionState_3, detectionState_4]

def getCurrentState():
    #get feature map
    #image = getCurrentImage()
    #feature_map = cnn(image)
    
    #get car_position
    car_position = getCurPosition()
    #get car orientation
    car_orientation = getCurOrientation()
    
    #get sensor3 sensor 4 distances
    collision_dist = getCollisionDistance()
    
    #get goal_position
    code, goal_handle = getHandle('goal')
    errorcode, goal_pos = vrep.simxGetObjectPosition(clientID,goal_handle,-1,vrep.simx_opmode_streaming)
    
    return [car_position, car_orientation, collision_dist, goal_pos]


def getMotorControls():
    
    code, left_handle = getHandle('left')
    code, right_handle = getHandle('right')
    
    #get left motor velocity (of car or motors ?)
    #errorcode, left_linear_velocity, left_angular_velocity = vrep.simxGetObjectVelocity(clientID,left_handle,vrep.simx_opmode_streaming)

    #get left motor velocity (of car or motors ?)
    #errorcode, right_linear_velocity, right_angular_velocity = vrep.simxGetObjectVelocity(clientID,right_handle,vrep.simx_opmode_streaming)
    
    returnCode,left_linear_velocity=vrep.simxGetObjectFloatParameter(clientID,left_handle,2012,vrep.simx_opmode_streaming)
    
    returnCode,right_linear_velocity=vrep.simxGetObjectFloatParameter(clientID,right_handle,2012,vrep.simx_opmode_streaming)
    
    startTime=time.time() 
    while time.time()-startTime < 1:   
        #get left motor velocity (of car or motors ?)
        #errorcode, left_linear_velocity, left_angular_velocity = vrep.simxGetObjectVelocity(clientID,left_handle,vrep.simx_opmode_streaming)

        #get left motor velocity (of car or motors ?)
        #errorcode, right_linear_velocity, right_angular_velocity = vrep.simxGetObjectVelocity(clientID,right_handle,vrep.simx_opmode_streaming)
       
        returnCode,left_linear_velocity=vrep.simxGetObjectFloatParameter(clientID,left_handle,2012,vrep.simx_opmode_buffer)
        
        returnCode,right_linear_velocity=vrep.simxGetObjectFloatParameter(clientID,right_handle,2012,vrep.simx_opmode_buffer)
        
        #print("left + ="+ str(np.linalg.norm(leftlinearVelocity)))
        left_linear_velocity = np.linalg.norm(left_linear_velocity)
        right_linear_velocity = np.linalg.norm(right_linear_velocity)
        #print("right + ="+ str(np.linalg.norm(rightlinearVelocity)))
        
    return [left_linear_velocity, right_linear_velocity]

def getAllSensorReadings(time_limit):
    
    sensor = [[] for x in range(10)]
    readings = []
    for i in range(1, 10):
        code, sensor[i] = getHandle('sensor' + str(i))
        
    
    #get proximity sensor(1-9) readings 
    for j in range(1,10):
        sensor_errorcode, detectionState, detectedPoint, detectedObjHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor (clientID,sensor[j],vrep.simx_opmode_streaming)
    
    
    start_time = time.time()
    while (time.time()-start_time) < time_limit: # while we are connected to the server..   
        #get proximity sensor3 readings
        readings_row = []
        for k in range(1,10):
            sensor_errorcode, detectionState, detectedPoint, detectedObjHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor (clientID,sensor[k],vrep.simx_opmode_buffer)
            #print( 'detectedPoint->', detectedPoint)
            #print( 'detectionState->', detectionState)
            #print('detectedSurfaceNormalVector', detectedSurfaceNormalVector)
            readings_row.append(detectionState)
            readings_row.append(detectedPoint)
            readings_row.append(detectedSurfaceNormalVector)
            
        readings_row = (np.hstack(readings_row))
        print('length of row->', len(readings_row))
        if len(readings_row)!=63:
            print('something wrong!!!! length is -->', len(readings_row))
            break
        readings.append(readings_row)
    #print(readings)
    return np.array(readings)
    '''code, sensor3 = getHandle('sensor3')
    code, sensor4 = getHandle('sensor4')
    
    startTime=time.time()
    #get proximity sensor3 readings 
    sensor_errorcode, detectionState, detectedPoint, detectedObjHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor (clientID,sensor3,vrep.simx_opmode_streaming)
    
    #get proximity sensor4 readings 
    sensor_errorcode, detectionState, detectedPoint, detectedObjHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor (clientID,sensor4,vrep.simx_opmode_streaming)
    
    while time.time()-startTime < 15:   
         #get proximity sensor3 readings 
         sensor_errorcode_3, detectionState_3, detectedPoint_3, detectedObjHandle, detectedSurfaceNormalVector_3 = vrep.simxReadProximitySensor (clientID,sensor3,vrep.simx_opmode_buffer)
    
         #get proximity sensor4 readings 
         sensor_errorcode_4, detectionState_4, detectedPoint_4, detectedObjHandle, detectedSurfaceNormalVector_4 = vrep.simxReadProximitySensor (clientID,sensor4,vrep.simx_opmode_buffer) 
         #if sensor_errorcode_4 == vrep.simx_return_ok and sensor_errorcode_3 == vrep.simx_return_ok:
         print(detectedSurfaceNormalVector_4) 
         print(detectedSurfaceNormalVector_3)
    
    return []'''

def startSimulation():
    returncode = vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)
    return returncode
    
def stopSimulation():
    returncode = vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
    return returncode
    
   
    
    