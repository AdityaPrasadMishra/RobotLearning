# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 01:19:43 2017

@author: peps
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import vrep
import sys
import sensor

def initEnv():
    vrep.simxFinish(-1)
    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
    if clientID!=-1:
        print ('Connected to remote API server')
    else:
        print('Connection unsuccessful')
        sys.exit('Could not Connect')
    
    sensor.setClient(clientID)
    #cur_pos = sensor.getCurPosition()
    #goal_pos = initGoalPos()
    return clientID
    