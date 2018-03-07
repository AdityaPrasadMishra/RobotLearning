import vrep,time,sys
import matplotlib.pyplot as plt
from PIL import Image as I
import array
import sys
import numpy as np
vrep.simxFinish(-1)

def streamVisionSensor (visionSensorName,clientID,pause=0.0001):
    
    #Get the handle of the vision sensor
    res1,visionSensorHandle=vrep.simxGetObjectHandle(clientID,visionSensorName,vrep.simx_opmode_oneshot_wait)
    print (visionSensorHandle)
    #Get the image
    res2,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_streaming)
    print (str(res2)+ str(res1))
    #Allow the display to be refreshed
    #plt.ion()
    #Initialiazation of the figure
    time.sleep(0.5)
    res,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_buffer)
    print ('End of Simulation')
    
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
if clientID!=-1:
    print ('Connected to remote API server')
else:
    print('Connection unsuccessful')
streamVisionSensor('Vision_sensor',clientID)