# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 02:42:34 2017

@author: AdityaPMishra
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 01:37:43 2017

@author: AdityaPMishra
"""

import vrep
import sys
import numpy as np
import time   
   
print ('Program started')
vrep.simxFinish(-1) 
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) 
if clientID!=-1:
    print ('Connected to remote API server')

    res,objs=vrep.simxGetObjects(clientID,vrep.sim_handle_all,vrep.simx_opmode_oneshot_wait)
    errorcode,cam_Handle = vrep.simxGetObjectHandle(clientID,'Vision_sensor',vrep.simx_opmode_oneshot_wait)
    if res==vrep.simx_return_ok:
        print ('Number of objects in the scene: ',len(objs))
    else:
        print ('Remote API function call returned with error code: ',res)

    time.sleep(2)
   
    startTime=time.time()   
    vrep.simxGetIntegerParameter(clientID,vrep.sim_intparam_mouse_x,vrep.simx_opmode_streaming) 
    ireturnCode,resolution,image=vrep.simxGetVisionSensorImage(clientID,cam_Handle,0,vrep.simx_opmode_streaming)
    while time.time()-startTime < 5:   
        returnCode,data=vrep.simxGetIntegerParameter(clientID,vrep.sim_intparam_mouse_x,vrep.simx_opmode_streaming) 
        ireturnCode,resolution,image=vrep.simxGetVisionSensorImage(clientID,cam_Handle,0,vrep.simx_opmode_buffer) 
        if ireturnCode==vrep.simx_return_ok: 
            print ('imagedata ',image) 

    vrep.simxAddStatusbarMessage(clientID,'Hello V-REP!',vrep.simx_opmode_oneshot)
    
    vrep.simxGetPingTime(clientID)
else:
    print('Connection unsuccessful')
    sys.exit('Could not Connect')