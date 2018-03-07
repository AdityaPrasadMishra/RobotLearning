"""
Created on Sat Apr 15 01:37:43 2017

@author: AdityaPMishra
"""

import vrep
import sys
import numpy as np
import time   
import matplotlib.pyplot as plt
   
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
    while time.time()-startTime < 10:   
        print(time.time())
        ireturnCode,resolution,image=vrep.simxGetVisionSensorImage(clientID,cam_Handle,0,vrep.simx_opmode_buffer)
        returnCode,leftlinearVelocity=vrep.simxGetObjectFloatParameter(clientID,leftMotorhandle,2012,vrep.simx_opmode_buffer)
        returnCode,rightlinearVelocity=vrep.simxGetObjectFloatParameter(clientID,rightMotorhandle,2012,vrep.simx_opmode_buffer)
        if ireturnCode==vrep.simx_return_ok:
            i=i+1
            inp = np.array(image, dtype=np.uint8)
            imagearray.append(inp)
            leftVelocityarray.append(leftlinearVelocity)
            print(leftlinearVelocity)
            rightVelocityarray.append(rightlinearVelocity)
            print(rightlinearVelocity)
            #inp.resize([resolution[0],resolution[1],3])
            #plt.imshow(inp,origin="lower")

    vrep.simxAddStatusbarMessage(clientID,'Hello V-REP!',vrep.simx_opmode_oneshot)
    
    vrep.simxGetPingTime(clientID)
    imagearray = np.array(imagearray)
    leftVelocityarray = np.array(leftVelocityarray)
    rightVelocityarray = np.array(rightVelocityarray)
    with open('imageslooper11.txt','wb') as f:
        np.savetxt('imageslooper11.txt',imagearray,'%i',delimiter=',')
    with open('leftVelocitylooper11.txt','wb') as f:
        np.savetxt('leftVelocitylooper11.txt',leftVelocityarray[None, :],'%f',delimiter=',')
    with open('rightVelocitylooper11.txt','wb') as f:
        np.savetxt('rightVelocitylooper11.txt',rightVelocityarray[None, :],'%f',delimiter=',')
else:
    print('Connection unsuccessful')
    sys.exit('Could not Connect')