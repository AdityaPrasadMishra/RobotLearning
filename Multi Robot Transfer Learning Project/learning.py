# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 21:20:22 2017

@author: peps
"""
from scipy.spatial import distance
import sensor


def getReward(state):
    
    cur_pos = state[1]
    reward = -1 
    time_reward = 1
    goal_pos = state[4]
    
    #should euclidean distance be taken 
    dis_reward = distance.euclidean( cur_pos, goal_pos )
    
    dis_to_collision = sensor.getCollisionDistance()
   
    if (dis_to_collision[0] ==0 or dis_to_collision[1] == 0):
        penalty = -100
    elif (dis_to_collision[0] < 1 or dis_to_collision[1] < 1):
        penalty = -40
    
    reward = dis_reward + time_reward + penalty
    return reward

def getMoveSpeed(move):
    
    #first entry stands for left motor
    #second ec=ntry stands for right motor
    motor_speeds = [0.5,0.5]
    if move == 0:
        print('slight left move')
        motor_speeds = [0.4, 0.6]
    elif move == 1:
        print('left move')
        motor_speeds = [0.2, 0.8]
    elif move == 2:
        print('straight move')
        motor_speeds = [0.5, 0.5]
    elif move == 3:
        print('slight right move')
        motor_speeds = [0.6, 0.4]
    elif move == 4:
        print('right move')
        motor_speeds = [0.8, 0.2]
    else:
        print ('Invalid move')
        
    return motor_speeds

def makeMove(cur_state, action):
    motor_speeds = getMoveSpeed(action)
    
    #set joint target velocity of the vehicle
    sensor.setJointVelocity(motor_speeds)
    
    new_state = sensor.getCurrentState()
    return new_state