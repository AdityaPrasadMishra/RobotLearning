# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import vrep
import sys
import numpy as np
vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
if clientID!=-1:
    print ('Connected to remote API server')
else:
    print('Connection unsuccessful')
    sys.exit('Could not Connect')
errorcode,left_motor_handle = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_oneshot_wait)
errorcode,right_motor_handle = vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_oneshot_wait)
errorcode = vrep.simxSetJointTargetVelocity(clientID,left_motor_handle,0.2,vrep.simx_opmode_streaming)
errorcode = vrep.simxSetJointTargetVelocity(clientID,right_motor_handle,0.2,vrep.simx_opmode_streaming)
errorcode,cam_Handle = vrep.simxGetObjectHandle(clientID,'Vision_sensor',vrep.simx_opmode_oneshot_wait)
print(cam_Handle)
returnCode,resolution,image=vrep.simxGetVisionSensorImage(clientID,cam_Handle,0,vrep.simx_opmode_streaming)
returnCode,resolution,image=vrep.simxGetVisionSensorImage(clientID,cam_Handle,0,vrep.simx_opmode_buffer)
print(image)

sensor_h=[] #empty list for handles
sensor_val=np.array([]) #empty array for sensor measurements
for x in range(1,16+1):
        errorCode,sensor_handle=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_ultrasonicSensor'+str(x),vrep.simx_opmode_oneshot_wait)
        sensor_h.append(sensor_handle) #keep list of handles        
        errorCode,detectionState,detectedPoint,detectedObjectHandle,detectedSurfaceNormalVector=vrep.simxReadProximitySensor(clientID,sensor_handle,vrep.simx_opmode_streaming)                
        sensor_val=np.append(sensor_val,np.linalg.norm(detectedPoint)) #get list of values